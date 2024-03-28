#!/bin/bash
set -e

docker build -f Dockerfile -t hello-gpu $TA1_REPOS_DIR
