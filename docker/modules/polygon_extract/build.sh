#!/bin/sh
set -e

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build -t inferlink/ta1_polygon_extract -f Dockerfile.tmp $REPO_ROOT/usc-umn-inferlink-ta1/
