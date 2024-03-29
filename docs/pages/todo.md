# Bugs and Open Issues


## High Priority

* **jira tickets**
* (18) need to verify input model files
   * legend_segment
   * line_extract
   * polygon_extract
* (20) legend_item_segment crashes on WY_CO_Peach - for Fandel
* (21) do we still need the text-spotting module? none of my command lines reference its outputs
* deployment
   * weiwei verify deployment process
* make S3 inputs bucket public/read
* server
    * expose the server
    * basicauth
    * OpenAI key
* S3 and CDR support
* overview pptx


# Low Priority

* FIXED? (9) legend_segment: uncharted-ta1/pipelines/segmentation/deploy/Dockerfile needs to be python3.10-slim
* server
    * user-defined module options
    * add ability to stop/abort a run
    * add ability to delete a run
    * add ability to delete a job
    * add ability to delete a job/module
* coalesce Dockerfiles
* root is owner of text spotting files
* inputs dir is $MAP_NAME/$MAP_NAME.tif