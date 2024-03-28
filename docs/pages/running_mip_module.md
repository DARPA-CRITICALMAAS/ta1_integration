# Running a Module (`mip_module`)

The `mip_module` tool runs exactly one module, for exactly one map image, using
the module's docker container.

The main command-line switches are:
* `--config-file`: path to the config file, e.g. `./config.yml`
* `--map-name`: name of the map image, e.g. `AK_Dillingham`
* `--job-name`: name of the job, e.g. `dillingham-0203`
* `--module-name`: name of the module to be run

Example:
```
$ ./mip/apps/mip_module.py --job-name alpha --module-name map_crop --map-name AK_Dillingham
```

The tool does NOT know about the inter-module dependencies: if a module
requires outputs from a predecessor module, and that predecessor module has not
been run under this job name, the target module will fail to execute correctly.
_In this sense, `mip_module.py` is really an "internal" tool: real users should
rely on `mip_job.py` (or the web server)._

`mip_module` supports a few other switches worth knowing:
* `--list-modules`: lists the names of the known modules and their predecessors
* `--openai-key-file`: path to the file containing your OpenAI key
* `--force-rerun`: forces the execution of the given target module, even if it has
    already been run successfully
