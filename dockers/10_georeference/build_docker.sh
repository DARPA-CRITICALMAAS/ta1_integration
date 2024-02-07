#!/bin/sh
set -e

../../docker-tools/dockerfile-include.py \
    Dockerfile Dockerfile.tmp ../../docker-tools

docker build -t inferlink/ta1_georeference -f Dockerfile.tmp $REPO_ROOT

