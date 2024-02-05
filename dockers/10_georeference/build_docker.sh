#!/bin/sh
set -e

$REPO_ROOT/integration/docker-tools/dockerfile-include.py \
    Dockerfile Dockerfile.tmp $REPO_ROOT/integration/docker-tools

docker build -t inferlink/ta1_georeference -f Dockerfile.tmp $REPO_ROOT

