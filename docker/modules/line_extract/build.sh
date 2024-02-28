#!/bin/sh
set -e

args=$@

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build $args -t inferlink/ta1_line_extract -f Dockerfile.tmp $REPO_DIR

rm -f Dockerfile.tmp
