#!/bin/sh
set -e
set -x

BUILD_CONTAINER=builder
IMAGE=inferlink/ta1_line_extract4

../../tools/dockerfile-include.py Dockerfile Dockerfile.tmp ../../tools

docker build -t $IMAGE -f Dockerfile.tmp $REPO_DIR

docker stop $BUILD_CONTAINER || true
docker rm $BUILD_CONTAINER || true

docker run --user root --name $BUILD_CONTAINER \
    --entrypoint /buildme.sh \
    -v REPO_DIR:/ta1/dev \
    -t $IMAGE

docker rmi $IMAGE:2 || true
docker commit $BUILD_CONTAINER $IMAGE:2

docker stop $BUILD_CONTAINER || true
docker rm $BUILD_CONTAINER || true

