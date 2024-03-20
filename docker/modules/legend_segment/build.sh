#!/bin/bash
set -e

args=$@

pushd $REPO_DIR/uncharted-ta1/pipelines/segmentation/deploy > /dev/null
./build.sh
popd > /dev/null

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build $args -t inferlink/ta1_legend_segment -f Dockerfile.tmp $REPO_DIR/uncharted-ta1/

rm -f Dockerfile.tmp
