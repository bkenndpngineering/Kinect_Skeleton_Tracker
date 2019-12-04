#!/bin/bash

# CD to the directory that contains this script
cd $(dirname $(readlink -f "$0"))

python3 -m skeleton_tracker -v tracking-module/trackhands /usr/lib
