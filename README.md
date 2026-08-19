# alpamayo2_trajectory_planning

<p align="center">
  <a href="https://www.ros.org"><img src="https://img.shields.io/badge/ROS 2-jazzy-22314e"/></a>
  <a href="https://github.com/thinking-cars/alpamayo2_trajectory_planning/releases/latest"><img src="https://img.shields.io/github/v/release/thinking-cars/alpamayo2_trajectory_planning"/></a>
  <a href="https://github.com/thinking-cars/alpamayo2_trajectory_planning/blob/main/LICENSE"><img src="https://img.shields.io/github/license/thinking-cars/alpamayo2_trajectory_planning"/></a>
  <br>
  <a href="https://github.com/thinking-cars/alpamayo2_trajectory_planning/actions/workflows/docker-ros.yml"><img src="https://github.com/thinking-cars/alpamayo2_trajectory_planning/actions/workflows/docker-ros.yml/badge.svg"/></a>
  <a href="https://github.com/thinking-cars/alpamayo2_trajectory_planning/actions/workflows/compose-oci.yml"><img src="https://github.com/thinking-cars/alpamayo2_trajectory_planning/actions/workflows/compose-oci.yml/badge.svg"/></a>
  <a href="https://github.com/thinking-cars/alpamayo2_trajectory_planning/actions/workflows/helm-oci.yml"><img src="https://github.com/thinking-cars/alpamayo2_trajectory_planning/actions/workflows/helm-oci.yml/badge.svg"/></a>
  <a href="https://thinking-cars.github.io/alpamayo2_trajectory_planning"><img src="https://github.com/thinking-cars/alpamayo2_trajectory_planning/actions/workflows/docs.yml/badge.svg"/></a>
  <a href="https://github.com/thinking-cars/alpamayo2_trajectory_planning/actions/workflows/consistency.yml"><img src="https://github.com/thinking-cars/alpamayo2_trajectory_planning/actions/workflows/consistency.yml/badge.svg"/></a>
</p>

**Alpamayo2-Super trajectory planning for ROS 2 and OpenADS.**

This repository provides a ROS 2 planning node that runs NVIDIA Alpamayo 2 Super from synchronized camera and odometry inputs and publishes a reference trajectory for downstream OpenADS modules.

<p align="center">
  <strong>🚀 <a href="#-quick-start">Quick Start</a></strong> • <strong>💻 <a href="#-development">Development</a></strong> • <strong>📝 <a href="#-documentation">Documentation</a></strong>
</p>

> [!IMPORTANT]
> This repository is part of [***OpenADS***](https://openads-project.github.io/), the *Open Automated Driving Systems* project. *OpenADS* and its modules have been initiated and are currently being maintained by the [**Institute for Automotive Engineering (ika) at RWTH Aachen University**](https://www.ika.rwth-aachen.de/de/).

## 🚀 Quick Start

1. Start a container of the pre-built runtime image.
    ```bash
    docker run --rm -it ghcr.io/thinking-cars/alpamayo2_trajectory_planning:latest bash
    ```
1. Inside the container, launch the pre-built nodes.
    ```bash
    ros2 launch alpamayo2_trajectory_planning alpamayo2_trajectory_planning_launch.py
    ```

## 💻 Development

### Set up Development Environment

1. Clone the repository.
    ```bash
    git clone https://github.com/thinking-cars/alpamayo2_trajectory_planning.git
    ```
1. Initialize the [`.openads-dev-environment`](https://github.com/openads-project/openads-dev-environment) submodule containing development environment configuration.
    ```bash
    cd alpamayo2_trajectory_planning
    git submodule update --init --recursive
    ```
1. Open the repository in [Visual Studio Code](https://code.visualstudio.com).
    ```bash
    code .
    ```
1. Install the recommended VS Code extensions.
    > *Ctrl+Shift+P / Extensions: Show Recommended Extensions / Install Workspace Recommended Extensions (Cloud Download Icon)*
1. Reopen the repository in a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers).
    > *Ctrl+Shift+P / Dev Containers: Rebuild and Reopen in Container*

### Build

> *Ctrl+Shift+B*

```bash
colcon build
```

### Run Tests

> *Ctrl+Shift+P / Tasks: Run Test Task*

```bash
colcon build --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=1
colcon test
colcon test-result --verbose
```


## 📝 Documentation

Package and node interfaces are documented in the respective package READMEs listed below. Implementation details are found in the [Source Code Documentation](https://thinking-cars.github.io/alpamayo2_trajectory_planning).

| Package | Description |
| --- | --- |
| [alpamayo2_trajectory_planning](alpamayo2_trajectory_planning/README.md) | ROS 2 trajectory planning using NVIDIA Alpamayo 2 Super |

## ⚖️ Licensing

The source code in this repository is licensed under Apache-2.0, see [LICENSE](LICENSE). Container images provided by this repository may contain third-party software shipped with their own license terms.

## 🙏 Acknowledgements

This project is maintained by [Thinking Cars](https://www.thinking-cars.de). We acknowledge the work of the [original authors at NVlabs](https://github.com/NVlabs).
