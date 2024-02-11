#!/bin/sh
set -e

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build -t inferlink/ta1_map_crop -f Dockerfile.tmp $REPO_DIR/usc-umn-inferlink-ta1/
