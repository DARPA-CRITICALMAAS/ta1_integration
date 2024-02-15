#!/bin/bash
set -e

docker build -f Dockerfile -t hello-gpu $REPO_DIR
