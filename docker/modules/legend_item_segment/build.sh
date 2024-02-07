#!/bin/sh
set -e

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build -t inferlink/ta1_legend_item_segment -f Dockerfile.tmp $REPO_ROOT
