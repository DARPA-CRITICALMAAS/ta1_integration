Setting up a new server:


1. Run `./main.py`
2. Set up your keys for ssh, github, etc
    1. mpg: `cd ~/dev/mpg-env ; ./do_setup 11.22.33.44`
3. log into server
4. `cd dev`
5. `git clone git@github.com:DARPA-CRITICALMAAS/ta1_integration`
6. `cd ta1_integration`
7. `git checkout -b XXX`
8. `curl -sSL https://install.python-poetry.org | python3 -`
9. `poetry shell`
9. `./server_setup.sh`

Verify docker and gpus
1. docker run hello-world
1. cd gpu
2. docker build -f Dockerfile -t hello-gpu .
3. docker run --gpus=all  hello-gpu

The build the docker containers:
1. `export REPO_DIR=$HOME/dev`
2. `cd docker/tools`
3. `./build_all.sh --build` or `--pull`
4. 