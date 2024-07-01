#!/bin/sh
set -e

args=$@

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build $args --no-cache -t inferlink/ta1_ptln_legend_item_description -f Dockerfile.tmp $TA1_REPOS_DIR

rm -f Dockerfile.tmp