# Conceptual Overview

## System Design: All the Layers

From the highest level, the entire system looks like this:

**Container/Module Layer:** There is a docker container for each module. The
container is expected to be run in a well-defined execution environment (i.e.
directory layout, explained below). Each module, and each container, operate
independently. The actual python code for the modules is (in most cases) in the
`usc-umn-inferlink-ta1` repo: we don't touch any of that code, we just interact
with it at the command line level.

**Mipper/Luigi Layer:** Sitting above the container layer is an application
("mipper") that executes the modules by running the containers. This app uses
the "luigi" python library to do task orchestration of the task graph. The task
graph is a DAG whose nodes are modules (run in docker containers) and whose
edges are input/output dependencies (expressed in the config.yml file). The
command line switches for running mipper are very simple.

**Web Server Layer:** Sitting above the mipper layer is a web server that
exposes a REST API for running the modules. Internally, the server just calls
the mipper app to do its work.

This system all runs on a single host machine.


## The Execution Environment

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
