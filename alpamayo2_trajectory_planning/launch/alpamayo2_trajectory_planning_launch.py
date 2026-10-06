#!/usr/bin/env python3

# Copyright (c) 2026 Thinking Cars GmbH
# SPDX-License-Identifier: Apache-2.0

import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetParameter


def generate_launch_description():
    """Create the launch description for the trajectory planning node."""

    remappable_topics = [
        DeclareLaunchArgument(
            "cross_left_image_topic",
            default_value="~/image/cross_left",
            description="cross-left camera image topic",
        ),
        DeclareLaunchArgument(
            "front_wide_image_topic",
            default_value="~/image/front_wide",
            description="front-wide camera image topic",
        ),
        DeclareLaunchArgument(
            "cross_right_image_topic",
            default_value="~/image/cross_right",
            description="cross-right camera image topic",
        ),
        DeclareLaunchArgument(
            "rear_left_image_topic",
            default_value="~/image/rear_left",
            description="rear-left camera image topic",
        ),
        DeclareLaunchArgument(
            "rear_right_image_topic",
            default_value="~/image/rear_right",
            description="rear-right camera image topic",
        ),
        DeclareLaunchArgument(
            "front_tele_image_topic",
            default_value="~/image/front_tele",
            description="front-telephoto camera image topic",
        ),
        DeclareLaunchArgument(
            "ego_data_topic",
            default_value="~/ego_data",
            description="ego motion input topic",
        ),
        DeclareLaunchArgument(
            "trajectory_topic",
            default_value="~/trajectory",
            description="predicted trajectory topic",
        ),
    ]

    args = [
        DeclareLaunchArgument("name", default_value="alpamayo2_trajectory_planning", description="node name"),
        DeclareLaunchArgument("namespace", default_value="", description="node namespace"),
        DeclareLaunchArgument(
            "params",
            default_value=os.path.join(get_package_share_directory("alpamayo2_trajectory_planning"), "config", "params.yml"),
            description="path to parameter file",
        ),
        DeclareLaunchArgument(
            "log_level", default_value="info", description="ROS logging level (debug, info, warn, error, fatal)"
        ),
        DeclareLaunchArgument("use_sim_time", default_value="false", description="use simulation clock"),
        DeclareLaunchArgument(
            "huggingface_token",
            default_value="",
            description="Hugging Face token used when the model is not cached",
        ),
        DeclareLaunchArgument(
            "model_cache_path",
            default_value="",
            description="Hugging Face model cache directory",
        ),
        *remappable_topics,
    ]

    nodes = [
        Node(
            package="alpamayo2_trajectory_planning",
            executable="alpamayo2_trajectory_planning",
            namespace=LaunchConfiguration("namespace"),
            name=LaunchConfiguration("name"),
            parameters=[
                LaunchConfiguration("params"),
                {
                    "huggingface_token": LaunchConfiguration("huggingface_token"),
                    "model_cache_path": LaunchConfiguration("model_cache_path"),
                },
            ],
            arguments=["--ros-args", "--log-level", LaunchConfiguration("log_level")],
            remappings=[(la.default_value[0].text, LaunchConfiguration(la.name)) for la in remappable_topics],
            output="screen",
            emulate_tty=True,
        )
    ]

    return LaunchDescription(
        [
            *args,
            SetParameter("use_sim_time", LaunchConfiguration("use_sim_time")),
            *nodes,
        ]
    )
