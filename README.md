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
3. A tool that can run (or re-run) one or more of the modules, in the correct
    order, via a simple command line
4. The ability to pull TA1 inputs from, and push TA1 outputs to, the CDR
5. A server exposing a REST API that can run mipper jobs

Documentation links:
* [Conceptual Overview](docs/pages/conceptual_overview.md)
* [System Setup](docs/pages/system_setup.md)
* [Running the Mipper Tool](docs/pages/running_mipper.md)
* [Running the Server](docs/pages/running_server.md)
* [Adding a New Module](docs/pages/adding_modules.md)
* [Other Topics](docs/pages/other_topics.md)
* [BUGS and ISSUES](docs/pages/todo.md)
