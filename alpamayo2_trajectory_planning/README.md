# `alpamayo2_trajectory_planning`

ROS 2 trajectory planning using NVIDIA Alpamayo 2 Super

- [Container Images](#container-images)
- [alpamayo2_trajectory_planning](#alpamayo2_trajectory_planning)

### Container Images

| Description | Image:Tag | Default Command |
| --- | --- | -- |
|  |  |  |

## Nodes

### `alpamayo2_trajectory_planning`



## Launch Files

### [`alpamayo2_trajectory_planning_launch.py`](launch/alpamayo2_trajectory_planning_launch.py)

| Argument | Default | Description |
| --- | --- | --- |
| `cross_left_image_topic` | `"~/image/cross_left"` | cross-left camera image topic |
| `front_wide_image_topic` | `"~/image/front_wide"` | front-wide camera image topic |
| `cross_right_image_topic` | `"~/image/cross_right"` | cross-right camera image topic |
| `rear_left_image_topic` | `"~/image/rear_left"` | rear-left camera image topic |
| `rear_right_image_topic` | `"~/image/rear_right"` | rear-right camera image topic |
| `front_tele_image_topic` | `"~/image/front_tele"` | front-telephoto camera image topic |
| `ego_data_topic` | `"~/ego_data"` | ego motion input topic |
| `trajectory_topic` | `"~/trajectory"` | predicted trajectory topic |
| `name` | `"alpamayo2_trajectory_planning"` | node name |
| `namespace` | `""` | node namespace |
| `params` | `os.path.join(get_package_share_directory("alpamayo2_trajectory_planning"), "config", "params.yml")` | path to parameter file |
| `log_level` | `"info"` | ROS logging level (debug, info, warn, error, fatal) |
| `use_sim_time` | `"false"` | use simulation clock |
