#!/bin/bash
set -e

pushd $REPO_ROOT/uncharted-ta1/pipelines/segmentation/deploy > /dev/null
./build.sh
popd > /dev/null

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build -t inferlink/ta1_legend_segment -f Dockerfile.tmp $REPO_ROOT/uncharted-ta1/
