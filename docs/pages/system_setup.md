# System Setup

To set up the system, you need to (Step 1) build out a host machine and then
(Step 2) configure the host machine.

We use a `p3.8xlarge` EC2 instance as our host. If you want to use your own
machine, you will need a comparable machine: at least one CPU (x64, Intel Xeon
class), at least one NVIDIA GPU (Tesla V100 or better), at least 128 GB of
RAM, and at least 250 GB of disk.


## STEP 1: Deploy the EC2 Instance

_Skip this step if you already have a host machine._

Our system runs on an EC2 instance. To make it easy to set up this machine, we
rely on a homegrown tool named "ilaws" which uses CloudFormation to define and
deploy the EC2 instance. If you are already familiar with EC2, you can build
the host using other tools: all that we require is a `p3.8xlarge` host with a
public IP address.

From your local machine, do the following:
1. mkdir /tmp/ta1_boot
2. cd /tmp/ta1_boot
3. Install ilaws: `pip install git+ssh://git@bitbucket.org/inferlink/ilaws.git/`
4. Get the two ilaws config files:
   1. `curl https://raw.githubusercontent.com/DARPA-CRITICALMAAS/ta1_integration/main/stack/template.yml > template.yml`
   2. `curl https://raw.githubusercontent.com/DARPA-CRITICALMAAS/ta1_integration/main/stack/config.yml > config.yml`
5. Edit `config.yml` to provide your own EC2 key pair name, a project name (any
    short string), and an owner name (any short string). You can also change
    the instance type, aws region, etc., in this file if you need to.
6. Start the instance, using any short string to name your stack (e.g. "ta1_test"):
    ```
   python -m ilaws create --stack-name YOUR_STACK_NAME --config-file stack/config.yml
    ```
   This will take 1-2 minutes.
7. Verify the instance is running:
    ```
    python -m ilaws info --stack-name ta1-test
    ```
   In the JSON output, it should say "running". You will also find the host's
   Public IP address in the output.

When you are not using the EC2 instance, you will want to suspend it (so you
don't get charged):
```
python -m ilaws suspend --stack-name ta1-test
```
You can then resume it from where you left off:
```
python -m ilaws resume --stack-name ta1-test
```
Note that it may take 1-2 minutes before the machine is ready to use; run the
"info" command to check and see if the status is "running" or not.

To completely kill the machine (and all data on it!):
```
python -m ilaws delete --stack-name ta1-test
```


## STEP 2: Configuring the Host

Now that your host is ready to use, we need to configure it: `ssh` into the
host and perform the following steps.

1. **Set up the needed directories**
    1. `mkdir /ta1 /ta1/inputs /ta1/outputs /ta1/temps /ta1/repos /ta1/runs`
    2. `cd /ta1/inputs`
    3. `aws s3 sync s3://inferlink-ta1-integration-inputs .`
    4. `cd /ta1/repos`
    5. `git clone git@github.com:DARPA-CRITICALMAAS/usc-umn-inferlink-ta1`
    6. `git clone git@github.com:DARPA-CRITICALMAAS/ta1_integration`
    7. `git clone git@github.com:DARPA-CRITICALMAAS/uncharted_ta1`

2. **Start your python environment**
    1. `curl -sSL https://install.python-poetry.org | python3 -`
    2. `cd /ta1/repos/ta1_integration`
    3. `poetry shell`
    4. `poetry install`
    5. `source ./envvars.sh`

3. **Pull all the prebuilt docker containers**
    1. `cd /ta1/repos/ta1_integration/docker/tools`
    2. `./build_all.sh --pull`

4. **Verify Docker is working**
    1. `docker run hello-world`

5. **Verify the GPUs are working**
    1. `nvidia-smi`
    2. `cd /ta1/repos/ta1_integration/docker/hello-gpu`
    3. `docker build -f docker/hello-gpu/Dockerfile -t hello-gpu .`
    4. `docker run --gpus=all hello-gpu --duration 5 --cpu` (should show CPU % well above 0)
    5. `docker run --gpus=all hello-gpu --duration 5 --gpu` (should show GPU % well above 0)

6. **Verify the mipper application works**
    1. `cd /ta1/repos/ta1_integration`
    2. `./mip/apps/mipper.py --list-modules`
    3. `./mip/apps/mipper.py --job-name 01 --map-name WY_CO_Peach --module-name start`
    4. `./mip/apps/mipper.py --job-name 01 --map-name WY_CO_Peach --module-name map_crop`

7. ** Verify the server and client work**
    1. `cd /ta1/repos/ta1_integration`
    2. `uvicorn mip.server.entry:app`
    3. _(in another ssh session)_ 
        1. `./mip/server/client.py --url http://127.0.0.1:8000 --get --output tmp.json`
        2. `./mip/server/client.py --url http://127.0.0.1:8000 --post --input ./mip/server/hello_input.json --output tmp.json`
