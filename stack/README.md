# Setting up a new server


## 1. Build the EC2 Stack

1. `./main.py --stack-name NAME ... --create`
2. `./main.py --stack-name NAME --public-ip`


## 2. Put the Build Environment onto the Server

1. ssh onto the server
2. If needed, set up your keys for ssh, GitHub, etc.
    1. _mpg only (localhost):_ `~/dev/mpg-env/do_setup 11.22.33.44`
3. `cd dev`
4. `git clone git@github.com:DARPA-CRITICALMAAS/ta1_integration`
5. `cd ta1_integration`
6. _if needed:_ `git checkout -b XXX`
7. `curl -sSL https://install.python-poetry.org | python3 -`
8. `poetry shell`
9. `poetry install`
10. `./server_setup.sh`


## 3. Verify Docker and GPUs Working

1. `docker run hello-world`
2. `nvidia-smi`
3. `cd gpu`
4. `docker build -f Dockerfile -t hello-gpu .`
5. `docker run --gpus=all  hello-gpu`


## 4. Get the TA1 Containers

1. `cd ~/dev`
2. `git clone git@github.com:DARPA-CRITICALMAAS/usc-umn-inferlink-ta1`
3. `export REPO_DIR=$HOME/dev`

Then, to pull the pre-built containers:

1. `cd ~/ta1_integration/docker/tools`
2. `./build_all.sh --pull`

Or, to build them yourself:

1. `cd ~/dev`
2. `git clone git@github.com:DARPA-CRITICALMAAS/uncharted-ta1`
3. `cd ~/ta1_integration/docker/tools`
4. `./build_all.sh --build`
5. _optional:_ `docker login`, `./build_all.sh --push` 


## 5. Verify the MIP System Works

1. `mkdir -p ~/dev/ta1_output ~/dev/ta1_temp
2. `aws s3 sync s3://inferlink-ta1-integration-inputs ~/dev/ta1_integration_input`
3. `cd ~/dev/ta1_integration`
4. `./mip/apps/mipper.py --list-modules`
5. `./mip/apps/mipper.py --job-name 01 --map-name WY_CO_Peach --module-name start`
6. `./mip/apps/mipper.py --job-name 01 --map-name WY_CO_Peach --module-name map_crop`
