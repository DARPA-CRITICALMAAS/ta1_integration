# Other Topics

## Notes on the Luigi Workflow Engine

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


## Building the Docker Containers

In the previous section, you pulled down the pre-built docker containers. If you
want to build them your self, do this:
1. `cd /ta1/dev`
2. `git clone git@github.com:DARPA-CRITICALMAAS/uncharted-ta1`
3. `cd /ta1/dev/ta1_integration/docker/tools`
4. `./build_all.sh --build`  (you can also use `--no-cache` here)

If you have write-access to docker hub, you can then do:
1. `docker login`,
2. `./build_all.sh --push`
