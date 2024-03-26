# Running the Mipper Tool

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
