This is the **Module Integration Project (MIP)**, which provides a means for
running all the TA1 modules from UMN/ISI/InferLink in a reproducible,
parallelized fashion:

* georeference
* legend_segment
* map_crop
* legend_item_segment
* legend_item_description
* line_extract
* polygon_extract
* point_extract
* geopackage

The main goals of this project are:

1. A clear definition of the input files, output files, and inter-module
    dependencies for each module, expressed in a single config file
2. The creation of a docker container to run each of the modules
3. A command-line tool (`mip_module`) that can run each dockerized module, in
    a well-defined environment
4. A command-line tool (`mip_job`) that can use `mip_module` to run (or re-run)
    a sequence of modules, in the correct order
5. A server (`mip_server`) that expose a REST API to run `mip_job`
6. The ability to pull TA1 inputs from, and push TA1 outputs to, the CDR

Documentation links:
* [Conceptual Overview](docs/pages/conceptual_overview.md)
* [System Setup](docs/pages/system_setup.md)
* [Running a Module (`mip_module`)](docs/pages/running_mip_module)
* [Running a Job (`mip_job`)](docs/pages/running_mip_job)
* [Running the Server (`mip_server`)](docs/pages/running_mip_server)
* [Adding a New Module](docs/pages/adding_modules.md)
* [Other Topics](docs/pages/other_topics.md)
* [BUGS and ISSUES](docs/pages/todo.md)
