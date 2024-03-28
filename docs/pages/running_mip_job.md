# Running a Job (`mip_job`)

The `mip_job` tool runs one or modules, including any needed predecessor
modules, by internally running the `mip_module` tool.

The key command-line switches are:
* `--config-file`: path to the config file, e.g. `./config.yml`
* `--map-name`: name of the map image, e.g. `AK_Dillingham`
* `--job-name`: name of the job, e.g. `dillingham-0203`
* `--module-name`: name of the module to be run, e.g. `map_crop`; may be
    repeated

Example:
```
$ ./mip/mip_job/mip_job.py --job-name alpha --module-name map_crop --map-name AK_Dillingham
```

The tool knows about the inter-module dependencies. It will run any run the
target module(s) given on the command line only after first running any required
predecessor modules, all in the proper order. The tool will skip the execution
of any module that has already successfully been run _for that job name_, as
indicated by the presence of a file named `MODULE.task` in the output
directory for that job.

`mip_job` supports a few other switches worth knowing:
* `--list-modules`: lists the names of the known modules and their predecessors
* `--list-deps`: displays a graph of the predecessors of the given target
    module, including information about which one have already been (successfully)
    run for the given job
* `--openai-key-file`: path to the file containing your OpenAI key
* `--force-rerun`: forces the execution of the given target module, even if it has
    already been run successfully
