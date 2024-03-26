# System Setup


## Deploying up the EC2 Instance

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


## Configuring the EC2 Host

Now that your EC2 host is ready to use, we need to configure it.

Using your EC2 key pair, `ssh` into the EC2 host and perform the following 
steps...


1. **Make the `cmaas` user**
    1. `sudo addgroup --gid 1024 cmaasgroup ; sudo adduser ubuntu cmaasgroup`


2. **Set up the needed directories**
    1. `mkdir /ta1/output /ta1/temp /ta1/dev /ta1/runs`
    2. `cd /ta1`
    3. TODO `git clone git@github.com:DARPA-CRITICALMAAS/ta1_integration_input`
    3. TODO `aws s3 sync s3://inferlink-ta1-integration-inputs /ta1/dev/ta1_integration_input`
    4. `cd /ta1/dev`
    5. `git clone git@github.com:DARPA-CRITICALMAAS/usc-umn-inferlink-ta1`
    6. `cd /ta1/dev`
    7. `git clone git@github.com:DARPA-CRITICALMAAS/ta1_integration`

3. **Start your python environment**
    1. `curl -sSL https://install.python-poetry.org | python3 -`
    2. `cd /ta1/dev/ta1_integration`
    3. `poetry shell`
    4. `source ./env.sh`

4. **Pull all the prebuilt docker containers**
    1. `cd /ta1/dev/ta1_integration/docker/tools`
    2. `./build_all.sh --pull`

5. **Verify Docker is working**
    1. `docker run hello-world`

6. **Verify the GPUs are working**
    1. `nvidia-smi`
    2. `cd /ta1_integration/docker/hello-gpu`
    3. `docker build -f docker/hello-gpu/Dockerfile -t hello-gpu .`
    4. `docker run --gpus=all hello-gpu --duration 5 --cpu` (should show CPU % well above 0)
    5. `docker run --gpus=all hello-gpu --duration 5 --gpu` (should show GPU % well above 0)

7. **Verify mipper works**
    1. `cd /ta1/dev/ta1_integration`
    2. `./mip/apps/mipper.py --list-modules`
    3. `./mip/apps/mipper.py --job-name 01 --map-name WY_CO_Peach --module-name start`
    4. `./mip/apps/mipper.py --job-name 01 --map-name WY_CO_Peach --module-name map_crop`
