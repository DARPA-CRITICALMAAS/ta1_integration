#!/bin/bash

set -e

sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y vim
sudo snap install emacs --classic

##sudo apt install hwinfo
##hwinfo --gfxcard --short

#sudo apt install -y build-essential
#sudo apt install nvidia-headless-535-server nvidia-utils-535-server -y
#sudo lshw -c video

##sudo apt install ubuntu-drivers-common
## sudo ubuntu-drivers list --gpgpu
##sudo ubuntu-drivers install --gpgpu
##sudo reboot

##sudo apt-get install -y nvidia-driver-510-server

##sudo snap install docker
##sudo groupadd docker
##sudo usermod -aG docker ubuntu
##sudo chmod 666 /var/run/docker.sock
##docker run hello-world