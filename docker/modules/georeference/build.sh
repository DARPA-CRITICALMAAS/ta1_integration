#!/bin/sh
set -e

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build -t inferlink/ta1_georeference -f Dockerfile.tmp $REPO_DIR/usc-umn-inferlink-ta1/
