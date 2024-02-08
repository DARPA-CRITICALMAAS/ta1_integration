#!/bin/sh
set -e

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build -t inferlink/ta1_geopackage -f Dockerfile.tmp $REPO_ROOT/usc-umn-inferlink-ta1/
