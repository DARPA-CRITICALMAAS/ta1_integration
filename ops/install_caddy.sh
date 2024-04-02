#!/usr/bin/env bash

set -e

# This script must be run using sudo

apt-get update -y
apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl
rm -f /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
       | sudo gpg --batch --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
        | sudo tee /etc/apt/sources.list.d/caddy-stable.list
apt-get update -y
apt-get install -y caddy
