#!/bin/bash

set -e

sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y vim
sudo snap install emacs --classic
