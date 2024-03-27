#!/bin/sh
set -e

args=$@

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build $args \
       -t inferlink/ta1_legend_item_description \
       --build-arg openai_api_key=`cat ~/.ssh/openai` \
       -f Dockerfile.tmp $TA1_REPOS_DIR/usc-umn-inferlink-ta1/

rm -f Dockerfile.tmp
