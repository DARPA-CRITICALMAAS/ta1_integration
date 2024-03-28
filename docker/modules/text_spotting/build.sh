#!/bin/sh
set -e

args=$@

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build $args -t inferlink/ta1_text_spotting -f Dockerfile.tmp $TA1_REPOS_DIR

rm -f Dockerfile.tmp
