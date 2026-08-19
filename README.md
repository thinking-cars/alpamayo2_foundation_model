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

**TODO: Repository tagline/description**

TODO: High-level repository introduction paragraph

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
    ros2 launch PACKAGE_NAME LAUNCH_FILE
    ```

<!-- TODO: replace default quick start with repo-specific demo (Docker Compose)

1. Launch a container of the pre-built runtime image in the provided demo [Docker Compose](demo/docker-compose.yml) setup.
    ```bash
    cd demo
    xhost +local: # allow GUI forwarding from containers
    docker compose up
    ```
1. Observe ...
1. Stop the demo and clean up.
    > *Ctrl+C*
    ```bash
    docker compose down
    xhost -local: # revoke GUI forwarding permissions
    ```
-->

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

## ⚖️ Licensing

The source code in this repository is licensed under Apache-2.0, see [LICENSE](LICENSE). Container images provided by this repository may contain third-party software shipped with their own license terms.

## 🙏 Acknowledgements

Development and maintenance of this repository are supported by the following projects. We acknowledge the funding of the respective institutions.

| Project | Funding Institution | Grant Number |
| --- | --- | --- |
| TODO | TODO | TODO |

<p>
  <img src="https://www.drought.uni-freiburg.de/stressres/images/bmftr-logo/image" height=70>
  <img src="https://ec.europa.eu/regional_policy/images/information-sources/logo-download-center/eu_funded_en.jpg" height=70>
</p>

<sub><sup>Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Climate, Infrastructure and Environment Executive Agency (CINEA). Neither the European Union nor CINEA can be held responsible for them.</sup></sub>
