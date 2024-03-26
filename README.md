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
* [Conceptual Overview](docs/pages/conceptual_overview)
* [System Setup](docs/pages/system_setup)
* [Running the Mipper Tool](docs/pages/running_mipper)
* [Running the Server](docs/pages/running_server)
* [Adding a New Module](docs/pages/adding_modules.md)
* [Other Topics](docs/pages/other_topics)


# Open Issues and Bugs

**HIGH PRIO**

* (9) legend_segment: uncharted-ta1/pipelines/segmentation/deploy/Dockerfile needs to be python3.10-slim
* (18) need to verify input model files
    * georeference
    * legend_segment
    * line extract
    * polygon extract
* implement server
* deployment
    * me verify deployment docs
    * weiwei verify deployment docs


**LOW PRIO**
* **jira tickets**
* coalesce dockerfile requirements
* switch to ansible
* make S3 inputs bucket public/read
* server
    * figure out CDR linkage 
    * add ability to stop/abort a run 
    * add ability to delete a run 
    * add ability to delete a job 
    * add ability to delete a job/module
