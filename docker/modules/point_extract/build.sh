#!/bin/sh
set -e

args=$@

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build $args -t inferlink/ta1_point_extract -f Dockerfile.tmp $TA1_REPOS_DIR/usc-umn-inferlink-ta1/

rm -f Dockerfile.tmp
