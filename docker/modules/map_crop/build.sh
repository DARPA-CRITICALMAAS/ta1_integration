#!/bin/sh
set -e

args=$@

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build $args -t inferlink/ta1_map_crop -f Dockerfile.tmp $REPO_DIR/usc-umn-inferlink-ta1/

rm -f Dockerfile.tmp
