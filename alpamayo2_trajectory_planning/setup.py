# Copyright (c) 2026 Thinking Cars GmbH
# SPDX-License-Identifier: Apache-2.0

import os
from glob import glob

from setuptools import setup

package_name = "alpamayo2_trajectory_planning"

setup(
    name=package_name,
    version="1.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        (os.path.join("share", package_name), ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*launch.[pxy][yma]*")),
        (os.path.join("share", package_name, "config"), glob("config/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="root",
    maintainer_email="vankempen@thinking-cars.de",
    description="ROS 2 trajectory planning using NVIDIA Alpamayo 2 Super",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["alpamayo2_trajectory_planning = alpamayo2_trajectory_planning.alpamayo2_trajectory_planning:main"],
    },
)
