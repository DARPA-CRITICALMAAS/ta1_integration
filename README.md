# CONTENTS

1. Introduction
2. [Conceptual Overview](docs/pages/overview.md)
3. System Setup
4. Running the Mipper Tool
5. Running the Server
6. Adding a New Module
7. Advanced Topics


# 1. Introduction

This is the **Module Integration Project (MIP)**, which provides a means for
running all the TA1 modules from UMN/ISI/InferLink in a reproducible,
parallelized fashion:

* georeference
* legend_segment
* map_crop
* text_spotting
* legend_item_segment
* legend_item_description
* line_extract
* polygon_extract
* point_extract
* geopackage

The five main goals of this project are:

1. A clear definition of the input files, output files, and inter-module
    dependencies for each module, expressed in a single config file
2. The creation of a docker container to run each of the modules
3. A tool (`mipper.py`) that can run (or re-run) one or more of the modules, in
    the correct order, via a simple command line
4. The ability to pull TA1 inputs from, and push TA1 outputs to, the CDR
5. A server exposing a REST API that can run mipper jobs



# 2. Conceptual Overview

## 2.1. System Design: All the Layers

From the highest level, the entire system looks like this:

**Container/Module Layer:** There is a docker container for each module. The
container is expected to be run in a well-defined execution environment (i.e.
directory layout, explained below). Each module, and each container, operate
independently. The actual python code for the modules is (in most cases) in the
`usc-umn-inferlink-ta1` repo: we don't touch any of that code, we just interact
with it at the command line level.

**Mipper/Luigi Layer:** Sitting above the container layer is an application
("mippper") that executes the modules by running the containers. This app uses
the "luigi" python library to do task orchestration of the task graph. The task
graph is a DAG whose nodes are modules (run in docker containers) and whose
edges are input/output dependencies (expressed in the config.yml file). The
command line switches for running mipper are very simple.

**Web Server Layer:** Sitting above the mipper layer is a web server that
exposes a REST API for running the modules. Internally, the server just calls
the mipper app to do its work.

This system all runs on a single host machine.


## 2.2. The Execution Environment

Your host machine will have three directories:

* `/ta1/input`: where the (static) input files live
* `/ta1/output`: where the results from each mipper job (run) will live
* `/ta1/temp`: scratch space used when running each job

_NOTE: Here we have used `/ta1` as the root of these three dirs, but in practice
they can each live anywhere._

When a module's container is run, these three directories will be mounted as
volumes so that the data is accessible from both the host and the container.

Each invocation of the `mipper` tool, to run one or more modules, is called a
"job". Each job is given a (simple, short) name, and the results from the job
are stored in a directory with that name. For example, if your job is named
`alpha`, you will find your results in `/ta1/output/alpha` (and
`/ta1/temp/alpha`).

When you run `mipper`, it will execute each of the known modules in the proper
order. The results from each module are in the job directory under the name of
the module. For example, if your job is named `alpha`, the results from the
map_crop module will include:

* `/ta1/output/alpha/map_crop.task.txt`: a text file whose presence indicates to
  the system that the map_crop operation succeeded. The contents of the file
  have some basic information about the run, including elapsed time.
* `/ta1/output/alpha/map_crop.docker.txt`: the log file from the dockerized
  execution of the module, i.e. anything that gets printed out to stdout or
  stderr. If the module crashes, this is where to look. (At the top of this file
  are command lines you can use to manually start the docker container,
  including its module options and volume mounts: this is very handy for
  debugging.)
* `/ta1/output/alpha/map_crop/`: the directory containing the output from the
  module itself.

Each module in the system has its own unique set of command line options. The
`config.yml` file is used to specify the various switch names and values. The
syntax allows for the use of a few variables, which are expanded at runtime to
point to the proper directories. Here is an example of a portion of the
`config.yml` file for a fictitious module that has three switches: one for the
map input, one for the results from a predecessor module, and one for the
output:

```yaml
extract_ore:
    input_tif: $INPUT_DIR/$MAP_NAME/$MAP_NAME.tif
    json_feed: $OUTPUT_DIR/feed_module/$MAP_NAME_foo.json
    output_dir: $OUTPUT_DIR/extract_ore
```

The  `mipper` tool (described below) takes command line switches to indicate
the config file location, the module(s) to be run, the map image to use, and the
name of the job.



# 3. MIP System Setup

## 3.1. Deploying up the EC2 Instance

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



## 3.2. Configuring the EC2 Host

_In the following, we will assume you are using `/ta1/...` as the root of the
mipper execution environment directories. Feel free to change these paths._

Now that your EC2 host is ready to use, we need to configure it.

Using your EC2 key pair, `ssh` into the EC2 host.

First, make the `cmaas` user:
1. `sudo addgroup --gid 1024 cmaasgroup ; sudo adduser ubuntu cmaasgroup`

Second, set up the directories needed:
1. `mkdir /ta1/output /ta1/temp /ta1/dev /ta1/runs`
2. `cd /ta1`
3. `git clone git@github.com:DARPA-CRITICALMAAS/ta1_integration_input`
3. `aws s3 sync s3://inferlink-ta1-integration-inputs /ta1/dev/ta1_integration_input`
4. `cd /ta1/dev`
5. `git clone git@github.com:DARPA-CRITICALMAAS/usc-umn-inferlink-ta1`
6. `cd /ta1/dev`
7. `git clone git@github.com:DARPA-CRITICALMAAS/ta1_integration`

Third, start your python environment:
1. `curl -sSL https://install.python-poetry.org | python3 -`
2. `cd /ta1/dev/ta1_integration`
3. `poetry shell`
4. `source ./env.sh`

Fourth, pull all the prebuilt docker containers:
1. `cd /ta1/dev/ta1_integration/docker/tools`
2. `./build_all.sh --pull`

Fifth, verify Docker is working:
1. `docker run hello-world`

Sixth, verify the GPUs are working:
1. `nvidia-smi`
2. `cd /ta1_integration/docker/hello-gpu`
4. `docker build -f docker/hello-gpu/Dockerfile -t hello-gpu .`
5. `docker run --gpus=all hello-gpu --duration 5 --cpu` (should show CPU % well above 0)
5. `docker run --gpus=all hello-gpu --duration 5 --gpu` (should show GPU % well above 0)

Seventh, verify mipper works:
1. `cd /ta1/dev/ta1_integration`
2. `./mip/apps/mipper.py --list-modules`
3. `./mip/apps/mipper.py --job-name 01 --map-name WY_CO_Peach --module-name start`
4. `./mip/apps/mipper.py --job-name 01 --map-name WY_CO_Peach --module-name map_crop`



# 4. Running the Mipper Tool

The `mipper` tool runs one job, consisting of one or more module executions for
one map image.

The main command-line switches are:
* `--config-file / -c`: path to the config file, e.g. `./config.yml`
* `--map-name / -i`: name of the map image, e.g. `AK_Dillingham`
* `--job-name / -j`: name of the job, e.g. `dillingham-0203`
* `--module-name / -m`: name of the module to be run, e.g. `map_crop`; may be
  repeated

Example:
```
$ ./mip/apps/mipper.py --job-name alpha --module-name map_crop --map-name AK_Dillingham
```

The tool knows about the inter-module dependencies. It will run any run the
target module(s) given on the command line only after first running any required
predecessor modules, all in the proper order. The tool will skip the execution
of any module that has already successfully been run _for that job name_, as
indicated by the presence of a file named `MODULE.task.txt` in the output
directory. 

The module name can be any one of the known modules, or the special module named
`end` which means "run everything". (There is also a special module named
`start` which is the root of the dependency tree. Running mipper with
`--module-name start` is a good test to make sure the system is working
properly.)

Mipper supports a few other switches worth knowing:
* `--list-modules`: lists the names of the known modules and their predecessors
* `--list-deps`: displays a graph of the predecessors of the given target
  module, including information about which one have already been (successfully)
  run for the given job
* `--openai-key-file`: path to the file containing your OpenAI key
* `--force`: forces the execution of the given target module, even if it has
  already been run successfully



# 5. Adding a New Module

This section explains how to add a new module, in three steps:
1. Writing the module
2. Making the docker container
3. Adding the module to mipper
4. Adding the module to the config file

In our examples below, we will call the new module `extract_ore`, its container
`inferlink/ta1_extract_ore`, and its class `ExtractOreTask`.


## 5.1. Your New Module

Your module should follow all the conventions of a robust python app (described
elsewhere), but in particular must follow this rule:

_Any references to external files, such as input images or model weights or
output PNGs, **must** be specified on the command line, so that the files can be
located relative to the mipper system's required directory layout. Do not use
any hard-coded paths and do not assume anything lives at "`.`"._


## 5.2. Your New Docker Containers

Each module needs to be run in its own docker container.

1. Add new directory `docker/modules/extract_ore`. (You can copy from one
   of the existing modules.)
2. Write a `Dockerfile` for your module and put it in the new dir. You should
   copy from one of the existing modules, but in general the file should contain
   these pieces, in order:
   1. The standard `FROM` line.
   2. The special line `# INCLUDEX base.txt`. This is an indicator to the mip
      docker build system to include the contents of another file into your
      file, to perform some functions common to all the docker containers.
   3. Whatever build requirements are needed for your module. 
   4. The special line `# INCLUDEX perms.txt`. This adds some user permission
      support and sets up the volumes used by all the docker containers.
   5. The two lines `CMD []` and `ENTRYPOINT ["python", "/path/to/module.py"]`.
3. Copy the file `build.sh` from one of the existing modules into your
   new directory. In the simplest case, you'll need to only change the name of
   the docker image in the `docker build` step.

Your container will be invoked such that it takes your command line switches and
runs your python app from the `.../output/JOB` directory, (roughly) like this:
```
docker run \
    -v /home/ubuntu/dev/ta1_integration_inputs:/ta1/input \
    -v /home/ubuntu/dev/ta1_output:/ta1/outout 
    -v /home/ubuntu/dev/ta1_temp:/ta1/temp \
    --gpus all \
    --user cmaas \
    inferlink/ta1_extract_ore \
    --option1 value --option2 value...
```

To build your container, you need to first set the environment variable
`$REPO_DIR` to point to the dir _above_ where you have the
`usc-umn-inferlink-ta1` repo checked out. That is, if `$REPO_DIR` is set to
`/home/user/dev`, your repository should be at 
`/home/user/dev/usc-umn-inferlink-ta1`.

Then, you can just run your `./build.sh`.

To build all the containers using mipper's build tools, run the build script
in that directory as `./build_all.sh --build`: this will build each of the
docker containers. (You can then run `./build_all.sh --push` to push all the
containers, if you have write access to InferLink's DockerHub repository.)


## 5.3. Your New Mipper Module

To add your new module to the mipper system, you need to write a task class, add
some verification code, and register the module. Fortunately, this is easy:

1. In the `mip/module_tasks` directory, add a new file `extract_ore_task.py`.
   You can copy the file from one of the other `_task.py` files. Your new file
   will define a class `ExtractOreTask` with three easy parts:
   1. Set the class variable `NAME` to the sting `"extract_ore"`.
   2. Set the class variable `REQUIRES` to a list of task class names, for each
      of the classes (modules) that your new module requires in order to run.
   3. Optionally, implement the method `run_post()`. This function is executed
      by mipper after your module has successfully completed running inside its
      docker container, and so is the ideal place to add simple checks to make
      sure that any expected output files exist in the right places.
   4. If your new module is a "leaf node" in the module dependency graph, edit
      the file `all.py` to add `ExtractOreTask` to the `REQUIRES` class variable
      of `AllTask`.


## 5.4. Your New Config File Section

Finally, you need to add your new module to the `config.yml` file. You will do
this by adding a new section to the file and, for each command line switch your
python app uses, add a line for it.

For example, assume `extract_ore.py` has four swiches: one for the map input,
one for the results from a predecessor module, one for the output directory, and
one for the frobble parameter. Your new section of the config file would look
like this:

```yaml
extract_ore:
    input_tif: $INPUT_DIR/$MAP_NAME/$MAP_NAME.tif
    json_feed: $OUTPUT_DIR/feed_module/$MAP_NAME_foo.json
    output_dir: $OUTPUT_DIR/extract_ore
    frobble_value: 3.14
```

_NOTE: if your switch takes no parameter (such as a boolean flag), you can't
leave the "value" part of in the YAML line empty: set it to `""` instead. 



# 6. Advanced Topics

# 6.1. Notes on the Luigi Workflow Engine

The mipper system uses the python `luigi` package to orchestrate the execution
of its tasks. The motivated reader is referred to the luigi docs for more
information: https://luigi.readthedocs.io/.

A few details about our use of luigi:
* Luigi is configured using the `luigi.cfg` file.
* Luigi's logger is configured using the `luigi_logging.conf` file.
* We are using the "local" scheduler, with only one process, until we're sure
  everything is stable. This means that modules will not be executed in
  parallel for a given map, even if the dependecy graph allows for it. (You can
  run multiple instances of mipper, however, using different job ids, to
  different maps in parallel.) 


## 6.2. OPTIONAL: Building the Docker Containers

In the previous section, you pulled down the pre-built docker containers. If you
want to build them your self, do this:
1. `cd /ta1/dev`
2. `git clone git@github.com:DARPA-CRITICALMAAS/uncharted-ta1`
3. `cd /ta1/dev/ta1_integration/docker/tools`
4. `./build_all.sh --build`  (you can also use `--no-cache` here)

If you have write-access to docker hub, you can then do:
1. `docker login`,
2. `./build_all.sh --push`
