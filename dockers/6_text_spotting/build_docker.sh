#!/bin/sh
set -e

../../docker-tools/dockerfile-include.py \
    Dockerfile Dockerfile.tmp ../../docker-tools

docker build -t inferlink/ta1_text_spotting -f Dockerfile.tmp $REPO_ROOT

