# Conceptual Overview

## System Design: All the Layers

From the highest level, the entire system looks like this:

**The Module (Container) Layer:** There is a docker container for each module.
The container is expected to be run in a well-defined execution environment
(i.e. directory layout, explained below). Each module, and each container,
operate independently. The actual python code for the modules is (in most
cases) in the `usc-umn-inferlink-ta1` repo: we don't touch any of that code, we
just interact with it at the command line level. **Our `mip_module` tool runs a
single given module.**

**The Job (Luigi) Layer:** Sitting above the module layer is an application
("mipper") that executes the modules by running the containers. This app uses
the "luigi" python library to do task orchestration of the task graph. The task
graph is a DAG whose nodes are modules (run in docker containers) and whose
edges are input/output dependencies (expressed in the config.yml file). We
define a "job" to be a named set of executed modules. Modules within a job can
be re-executed if they fail. **Our `mip_job` tool runs one or more modules (via
`mip_module`), including any required predecessor modules.**

**The Server Layer:** Sitting above the job layer is a web server that exposes
a REST API for running the modules. Internally, the server just calls `mip_job`
to do its work. **Our `mip_server` tool runs the web server.**

This system all runs on a single host machine.


## The Execution Environment

Your host machine will have several directories:

* `/ta1/inputs`: where the (static) input files live
* `/ta1/outputs`: where the results from each execution of `mip_module` and
    `mip_job` will live
* `/ta1/temps`: scratch space used when running modules
* `/ta1/runs`: where the results from each (`mip-server`-based) execution of
    `mip_job` will live

_NOTE: Here we have used `/ta1` as the root of these three dirs, but in theory
they can each live anywhere._

When a module's container is run, some of these directories will be mounted as
volumes so that the data is accessible from both the host and the container.

Each invocation of the `mip_module` tool, to run exactly one module from within
its docker container, will have a job name (short text string). The results
from the run are stored in a directory with that name. For example, if your job
is named `alpha` and your target module is named `map_crop`, you will find your
module's outputs in `/ta1/outputs/alpha/map_crop`. You will also find a status
file (`/ta1/outputs/alpha/map_crop.json`) holding the execution state of the
module.

Each invocation of the `mip_job` tool will run one or more modules, also under
a given job name. Because `mip_job` uses `mip_module` to run each module, the
outputs for any module ever run for a given job name will all live in that same
job directory. You will also find a status file (`/ta1/outputs/alpha.json`)
holding the execution state of the job. (When a module is run using `mip_job`),
will also find a luigi state file (`/ta1/outputs/alpha/map_crop.task`); this is
only used internally.)

When you run `mip_jobs`, it will execute each of the known modules in the
proper order. The results from each module are in the job directory under the
name of the module. For example, if your job is named `alpha`, the results from the
map_crop module will include:

Each module in the system has its own unique set of command line options. The
`config.yml` file is used to specify the various switch names and values. The
syntax allows for the use of a few variables, which are expanded at runtime to
point to the proper directories. Here is an example of a portion of the
`config.yml` file for a fictitious module that has three switches: one for the
map input, one for the results from a predecessor module, and one for the
output:

```yaml
refine_ore:
    input_tif: $INPUT_DIR/$MAP_NAME/$MAP_NAME.tif
    extracted_ore_file: $OUTPUT_DIR/extract_ore/$MAP_NAME_ore.json
    output_dir: $OUTPUT_DIR/refine_ore
    throttle: 17
```

The `mip_module` tool would thus pass these switches to the docker container
for the `refine_ore` algorithm, when used on the famous `WY_CO_Peach` map:

```
--input-tif /ta1/inputs/WY_CO_Peach/WY_CO_Peach.tif
--extracted-ore-file /ta1/outputs/extracted_ore/WY_CO_Peach_ore.tif
--output_dir /ta1/outputs/refined_ore
--throttle 17
```

Note carefully how the command-line arguments have been subjected to variable
interpolation. Note also that the directory paths are specified relative to the
container environment, not the host environment.
