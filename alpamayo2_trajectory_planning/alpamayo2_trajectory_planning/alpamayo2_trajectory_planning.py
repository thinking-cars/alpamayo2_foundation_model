# Copyright (c) 2026 Thinking Cars GmbH
# SPDX-License-Identifier: Apache-2.0

"""ROS 2 adapter for Alpamayo 2 Super trajectory inference."""

import sys
from collections import deque
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Any, Optional

import rclpy
import torch
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from trajectory_planning_msgs.msg import REFERENCE, Trajectory

CAMERA_IDS = (0, 1, 2, 3, 5, 6)
CAMERA_NAMES = (
    "camera_cross_left_120fov",
    "camera_front_wide_120fov",
    "camera_cross_right_120fov",
    "camera_rear_left_70fov",
    "camera_rear_right_70fov",
    "camera_front_tele_30fov",
)
WAYPOINT_DT_SECONDS = 0.1


class Alpamayo2TrajectoryPlanning(Node):
    """Buffer ROS sensor data and publish Alpamayo 2 Super trajectories."""

    def __init__(self) -> None:
        """Configure sensor subscriptions, publishers, and Alpamayo inference."""
        super().__init__("alpamayo2_trajectory_planning")
        self.declare_parameter("model_name", "nvidia/Alpamayo2-Super")
        self.declare_parameter("model_source_path", "")
        self.declare_parameter("image_topics", [""])
        self.declare_parameter("odometry_topic", "~/odometry")
        self.declare_parameter("trajectory_topic", "~/trajectory")
        self.declare_parameter("output_frame_id", "base_link")
        self.declare_parameter("inference_period_sec", 2.0)
        self.declare_parameter("max_generation_length", 256)
        self.declare_parameter("num_diffusion_steps", 10)
        self.declare_parameter("top_p", 0.98)
        self.declare_parameter("temperature", 0.6)
        self.declare_parameter("max_image_long_side", 1280)
        self.declare_parameter("odometry_history_stride", 5)

        if not torch.cuda.is_available():
            raise RuntimeError("Alpamayo 2 Super requires a CUDA-capable NVIDIA GPU.")

        self._device = torch.device("cuda")
        self._dtype = torch.bfloat16
        self._num_frames = 4
        self._num_history_steps = 16
        self._history_stride = int(self.get_parameter("odometry_history_stride").value)
        if self._history_stride < 1:
            raise ValueError("odometry_history_stride must be at least one")

        image_topics = list(self.get_parameter("image_topics").value)
        self._validate_image_topics(image_topics)
        self._image_topics = image_topics
        self._frame_buffers: dict[str, deque[tuple[Any, torch.Tensor]]] = {
            topic: deque(maxlen=self._num_frames * 3) for topic in image_topics
        }
        self._odometry_buffer: deque[Odometry] = deque(maxlen=self._num_history_steps * self._history_stride + 10)
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._active_future: Optional[Future[dict[str, Any]]] = None

        trajectory_topic = str(self.get_parameter("trajectory_topic").value)
        self._publisher = self.create_publisher(Trajectory, trajectory_topic, 10)
        for topic in image_topics:
            self.create_subscription(
                Image,
                topic,
                lambda message, image_topic=topic: self._image_callback(image_topic, message),
                qos_profile_sensor_data,
            )
            self.get_logger().info(f"Subscribed to image topic '{topic}'")

        odometry_topic = str(self.get_parameter("odometry_topic").value)
        self.create_subscription(Odometry, odometry_topic, self._odometry_callback, qos_profile_sensor_data)
        self.get_logger().info(f"Subscribed to odometry topic '{odometry_topic}'")
        self.get_logger().info(f"Publishing trajectories on '{trajectory_topic}'")

        self._load_model()
        inference_period = float(self.get_parameter("inference_period_sec").value)
        if inference_period <= 0.0:
            raise ValueError("inference_period_sec must be positive")
        self._timer = self.create_timer(inference_period, self._timer_callback)

    def declare_and_load_parameter(self, name: str, default_value: Any) -> Any:
        """Declare a parameter and return its configured value."""
        self.declare_parameter(name, default_value)
        return self.get_parameter(name).value

    def destroy_node(self) -> bool:
        """Stop background inference before releasing ROS resources."""
        self._executor.shutdown(wait=False, cancel_futures=True)
        return super().destroy_node()

    @staticmethod
    def _validate_image_topics(image_topics: list[str]) -> None:
        if len(image_topics) != len(CAMERA_IDS) or any(not topic for topic in image_topics):
            raise ValueError(
                "image_topics must contain six non-empty topics ordered as "
                "cross-left, front-wide, cross-right, rear-left, rear-right, front-tele."
            )

    def _load_model(self) -> None:
        model_source_path = str(self.get_parameter("model_source_path").value)
        candidate_paths = [Path(model_source_path).expanduser()] if model_source_path else []
        candidate_paths.append(Path(__file__).resolve().parents[2] / "src")
        for candidate_path in candidate_paths:
            if (candidate_path / "alpamayo2_super").is_dir():
                sys.path.insert(0, str(candidate_path))
                break

        try:
            from alpamayo2_super import helper
            from alpamayo2_super.models.alpamayo2_super import Alpamayo2Super
        except ModuleNotFoundError as error:
            raise RuntimeError(
                "Alpamayo 2 Super is not importable. Install it in the runtime environment or set "
                "model_source_path to the directory containing alpamayo2_super."
            ) from error

        model_name = str(self.get_parameter("model_name").value)
        self.get_logger().info(f"Loading Alpamayo 2 Super model '{model_name}' on CUDA")
        self._model = Alpamayo2Super.from_pretrained(
            model_name,
            dtype=self._dtype,
            device_map="cuda:0",
            attn_implementation="sdpa",
        )
        self._model.eval()
        self._helper = helper
        self._tokenizer = self._model.tokenizer
        self.get_logger().info("Alpamayo 2 Super model loaded")

    def _image_callback(self, topic: str, message: Image) -> None:
        try:
            frame = self._ros_image_to_tensor(message)
        except ValueError as error:
            self.get_logger().error(f"Ignoring image from '{topic}': {error}")
            return
        self._frame_buffers[topic].append((message.header.stamp, frame))

    def _odometry_callback(self, message: Odometry) -> None:
        self._odometry_buffer.append(message)

    @staticmethod
    def _ros_image_to_tensor(message: Image) -> torch.Tensor:
        encoding = message.encoding.lower()
        channels_by_encoding = {
            "rgb8": 3,
            "bgr8": 3,
            "rgba8": 4,
            "bgra8": 4,
            "mono8": 1,
        }
        try:
            channels = channels_by_encoding[encoding]
        except KeyError as error:
            raise ValueError(f"unsupported encoding '{message.encoding}'; use rgb8, bgr8, rgba8, bgra8, or mono8") from error
        if message.step < message.width * channels:
            raise ValueError("row step is smaller than the encoded image width")

        image = torch.frombuffer(bytearray(message.data), dtype=torch.uint8).clone()
        expected_size = message.height * message.step
        if image.numel() != expected_size:
            raise ValueError(f"data contains {image.numel()} bytes, expected {expected_size}")
        image = image.reshape(message.height, message.step)[:, : message.width * channels]
        image = image.reshape(message.height, message.width, channels)
        if encoding in {"bgr8", "bgra8"}:
            image = image[..., [2, 1, 0]]
        elif encoding in {"rgba8", "bgra8"}:
            image = image[..., :3]
        elif encoding == "mono8":
            image = image.repeat(1, 1, 3)
        return image.permute(2, 0, 1).contiguous()

    def _timer_callback(self) -> None:
        if self._active_future is not None and not self._active_future.done():
            return
        payload = self._prepare_payload()
        if payload is None:
            return
        self._active_future = self._executor.submit(self._run_inference, payload)
        self._active_future.add_done_callback(self._handle_inference_result)

    def _prepare_payload(self) -> Optional[dict[str, Any]]:
        if not all(len(buffer) >= self._num_frames for buffer in self._frame_buffers.values()):
            return None
        if len(self._odometry_buffer) < self._num_history_steps * self._history_stride:
            return None

        frame_sets = [list(self._frame_buffers[topic])[-self._num_frames :] for topic in self._image_topics]
        try:
            image_frames = torch.stack([torch.stack([frame for _, frame in frames]) for frames in frame_sets])
        except RuntimeError as error:
            self.get_logger().error(f"Image streams must have equal frame dimensions: {error}")
            return None
        image_frames = self._downscale(image_frames)
        odometry_history = list(self._odometry_buffer)[-self._num_history_steps * self._history_stride :: self._history_stride]
        ego_history_xyz, ego_history_rot = self._build_ego_history(odometry_history)
        stamps = [frames[-1][0] for frames in frame_sets]
        stamp = min(stamps, key=lambda value: (value.sec, value.nanosec))
        return {
            "image_frames": image_frames,
            "camera_indices": torch.tensor(CAMERA_IDS, dtype=torch.int64),
            "camera_names": list(CAMERA_NAMES),
            "ego_history_xyz": ego_history_xyz,
            "ego_history_rot": ego_history_rot,
            "stamp": stamp,
        }

    def _downscale(self, image_frames: torch.Tensor) -> torch.Tensor:
        max_long_side = int(self.get_parameter("max_image_long_side").value)
        height, width = image_frames.shape[-2:]
        if max_long_side <= 0 or max(height, width) <= max_long_side:
            return image_frames
        scale = max_long_side / max(height, width)
        target_size = (max(1, round(height * scale)), max(1, round(width * scale)))
        flattened = image_frames.flatten(0, 1).float()
        resized = torch.nn.functional.interpolate(flattened, size=target_size, mode="bicubic", align_corners=False)
        return resized.clamp(0, 255).to(torch.uint8).reshape(*image_frames.shape[:2], 3, *target_size)

    @staticmethod
    def _build_ego_history(odometry_history: list[Odometry]) -> tuple[torch.Tensor, torch.Tensor]:
        positions = torch.tensor(
            [
                [message.pose.pose.position.x, message.pose.pose.position.y, message.pose.pose.position.z]
                for message in odometry_history
            ],
            dtype=torch.float32,
        )
        quaternions = torch.tensor(
            [
                [
                    message.pose.pose.orientation.x,
                    message.pose.pose.orientation.y,
                    message.pose.pose.orientation.z,
                    message.pose.pose.orientation.w,
                ]
                for message in odometry_history
            ],
            dtype=torch.float32,
        )
        rotations = Alpamayo2TrajectoryPlanning._quaternions_to_rotations(quaternions)
        t0_rotation_inverse = rotations[-1].transpose(0, 1)
        local_positions = (positions - positions[-1]) @ t0_rotation_inverse.transpose(0, 1)
        local_rotations = t0_rotation_inverse.unsqueeze(0) @ rotations
        return local_positions.unsqueeze(0).unsqueeze(0), local_rotations.unsqueeze(0).unsqueeze(0)

    @staticmethod
    def _quaternions_to_rotations(quaternions: torch.Tensor) -> torch.Tensor:
        normalized = torch.nn.functional.normalize(quaternions, dim=1)
        x, y, z, w = normalized.unbind(dim=1)
        return torch.stack(
            (
                1 - 2 * (y * y + z * z),
                2 * (x * y - z * w),
                2 * (x * z + y * w),
                2 * (x * y + z * w),
                1 - 2 * (x * x + z * z),
                2 * (y * z - x * w),
                2 * (x * z - y * w),
                2 * (y * z + x * w),
                1 - 2 * (x * x + y * y),
            ),
            dim=1,
        ).reshape(-1, 3, 3)

    def _run_inference(self, payload: dict[str, Any]) -> dict[str, Any]:
        model_inputs = self._helper.prepare_model_inputs(payload, self._model.config, self._tokenizer)
        model_inputs = self._helper.to_device(model_inputs, device=self._device)
        with torch.autocast(device_type="cuda", dtype=self._dtype):
            predicted_xyz, _predicted_rotations, _logprob, _extra = self._model.sample_trajectories_from_data(
                data=model_inputs,
                top_p=float(self.get_parameter("top_p").value),
                temperature=float(self.get_parameter("temperature").value),
                num_traj_samples=1,
                num_traj_sets=1,
                max_generation_length=int(self.get_parameter("max_generation_length").value),
                diffusion_kwargs={"inference_step": int(self.get_parameter("num_diffusion_steps").value)},
                return_extra=True,
            )
        return {
            "trajectory": predicted_xyz.detach().cpu()[0, 0, 0],
            "stamp": payload["stamp"],
        }

    def _handle_inference_result(self, future: Future[dict[str, Any]]) -> None:
        try:
            result = future.result()
        except Exception as error:
            self.get_logger().error(f"Alpamayo 2 Super inference failed: {error}")
            return
        trajectory = self._to_trajectory_message(result["trajectory"], result["stamp"])
        self._publisher.publish(trajectory)
        self.get_logger().info(f"Published {len(result['trajectory'])} Alpamayo waypoints")

    def _to_trajectory_message(self, points: torch.Tensor, stamp: Any) -> Trajectory:
        trajectory = Trajectory()
        trajectory.header.stamp = stamp
        trajectory.header.frame_id = str(self.get_parameter("output_frame_id").value)
        trajectory.type_id = REFERENCE.TYPE_ID
        trajectory.score = 0
        states: list[float] = []
        previous_point = torch.zeros(2)
        speeds: list[float] = []
        for index, point in enumerate(points):
            xy = point[:2]
            speed = float(torch.linalg.vector_norm(xy - previous_point).item() / WAYPOINT_DT_SECONDS)
            speeds.append(speed)
            states.extend((float((index + 1) * WAYPOINT_DT_SECONDS), float(xy[0]), float(xy[1]), speed))
            previous_point = xy
        trajectory.states = states
        trajectory.standstill = max(speeds, default=0.0) < 0.1
        return trajectory


def main(args: Optional[list[str]] = None) -> None:
    """Initialize and spin the Alpamayo trajectory planning node."""
    rclpy.init(args=args)
    node = Alpamayo2TrajectoryPlanning()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
