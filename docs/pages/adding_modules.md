# Adding New Modules

This section explains how to add a new module, in three steps:
1. Writing the module
2. Making the docker container
3. Adding the module to mipper
4. Adding the module to the config file

In our examples below, we will call the new module `extract_ore`, its container
`inferlink/ta1_extract_ore`, and its class `ExtractOreTask`.


## 1. Your New Module

Your module should follow all the conventions of a robust python app (described
elsewhere), but in particular must follow this rule:

_Any references to external files, such as input images or model weights or
output PNGs, **must** be specified on the command line, so that the files can be
located relative to the mipper system's required directory layout. Do not use
any hard-coded paths and do not assume anything lives at "`.`"._


## 2. Your New Docker Containers

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
    inferlink/ta1_extract_ore \
    --option1 value --option2 value...
```

To build, just run your `./build.sh`.

To build all the containers using mipper's build tools, run the build script
in that directory as `./build_all.sh --build`: this will build each of the
docker containers. (You can then run `./build_all.sh --push` to push all the
containers, if you have write access to InferLink's DockerHub repository.)


## 3. Your New Mipper Module

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


## 4. Your New Config File Section

Finally, you need to add your new module to the `config.yml` file. You will do
this by adding a new section to the file and, for each command line switch your
python app uses, add a line for it.

For example, assume `extract_ore.py` has four switches: one for the map input,
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
