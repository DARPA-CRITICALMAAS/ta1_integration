# The Web Server

## 1. Goals

We want a web API for running our TA1 modules. It should provide all the core
functionality we need, including supporting the needs of the CDR.

Specifically, the API should:
* 
* Follow the REST conventions, in terms of styling the URLs
* Not expose any implementation details (such as whether the modules are
    executed in-line or with local docker containers or via ECS or…)
* Be asynchronous (non-blocking)
* Provide support for running each individual module as well as the whole
    end-to-end graph of modules 
* Provide a means for downloading the logs, outputs, and temp files from each
    run 
* Store the data to S3 and/or CDR 
* Be invokable via CDR 
* Allow for re-running failed jobs 
* Provide a mechanism for passing “extra” switches to the modules' command line
* Returned data (and POST input payloads) will be JSON, with schemas
* Use “basicauth” for simple user/password protection 

The system is NOT expected to do everything, however: you will need to ssh into
the server to handle source code updates, rebuild docker containers, etc.

Also, we will write a little command line tool that acts as a very simple
front-end to the web api, for testing and for users.


## 2. Overview

There will be two sets of endpoints:

**The “execution” API** is used only to execute a module. Executing a module,
via POST, will require a payload with the job name and module name, and will
return a run-id. Query the run-id, via GET, will return the status of the run
(started, passed, failed).

The special module name “ALL” corresponds to running all the modules.

_Implementation: A “run” corresponds to a single invocation of the “mipper”
tool – which, in turn, uses luigi to locally run the required modules. This
allows us to optionally run any needed predecessor modules, and to run things
in parallel if desired._

**The “job” API** is used only to access the results from the execution of a
module. Querying by job name and module name, via GET, will return of the
module’s log file(s), the output files, etc. This API just reads files from
disk, it does not do any real computational work.

_Rationale: We keep these two APIs separate in order to separate the “execution
of the mipper/luigi system” and the “retrieval of the module outputs”, because
we want to allow the user to run the same job/module combination more than once
(and including implicitly running or re-running any predecessor modules). At
the lowest level, we want to be able to keep all the mipper/luigi execution
logs distinct from the module-specific logs, yet also be able to have a simple
means of determining if a submitted run has completed. Without this separation,
the code would get messier; in the longer term, though, I’d like to do
something better._


## 3. Running the Server

## 4. Running the Client

## 5. The REST Endpoints

### 5.1. The Run API

#### `POST /run`

Runs the given module(s). Will also run any required predecessor modules that
haven’t yet been run.
* Payload: a RunPayload object
* Returns: a RunStatus object
* _Implementation: Generate a new run-id. Write a RunStatus object to the file
    `/ta1_runs/{run_id}.json`, with status=started, and return that object.
    Will also start a background thread to run the mipper process, and when
    process ends we’ll update the json file and end the thread._

#### `GET /run`

Returns a list of all the run-ids.
* Returns: a JSON list of run-id strings
* _Implementation: Collect all the run-ids by expanding `/ta1_runs/*.json`_

#### `GET /run/{run-id}`

Returns the status of the given run-id.
* Returns: a RunStatus object
* _Implementation: Return the contents of `/ta1_runs/{run_id}.json`_


### 5.2. The Job API

#### `GET /jobs`

Get a list of all jobs that have been run
* Returns: a JSON list of all the job names
* _Implementation: Expand out `/ta1_outputs/*`

#### `GET /jobs/{job_name}`

Get a list of all modules that have been run for the given job
* Returns: a JSON list of all the module names
* _Implementation: Expand out `/ta1_outputs/{job_name}/*.status.json`_

#### `GET /jobs/{job_name}/{module_name}`

Gets info about a module run under a given job name
* Returns: a ModuleStatus object
* _Implementation: Return contents of `/ta1_outputs/{job_name}/{module_name}.status.json`

#### `GET /jobs/{job_name}/{module_name}/logs`

Gets the logs from the last run of the given job/module
* Returns: a zip file containing the log file(s)

#### `GET /jobs/{job_name}/{module_name}/outputs`

Gets the outputs from the last run of the given job/module
* Returns: a zip file containing the output file(s)

#### `GET /jobs/{job_name}/{module_name}/temps`

Gets the temp files from the last run of the given job/module
* Returns: a zip file containing the temp file(s)

#### `GET /modules`

Helper function to get list of the supported modules
* Returns: list of ModuleDescription objects


### 5.3. The Schemata

The following Pydantic classes (JSON dicts) are used for endpoint payloads and responses.

#### `RunPayload`

* job: str
* modules: list of str
* map: str
* force_rerun: optional bool (default: False) -- if set, will force the module
  to be run, even if the job/module has already been successfully run
* module_options: optional dict of (str, str) (default: empty dict) -- mapping
    from module name to a string with extra command-line switches for that
    module
* **TODO:** will probably require env var interpolation, for dir paths

#### `RunStatus`

* status: enum of (not started, running, passed, failed)
* run_id: str
* post_payload: RunPayload
* start_time: timestamp
* stop_time: timestamp (or None, if run not finished)
* log: str (or None, if run not finished?)
* embedded contents of log file, appropriately escaped

#### `ModuleStatus`

* status: enum of (running, passed, failed)
* job str
* module: str
* start_time: timestamp
* stop_time: timestamp (or None, if not finished)
* ??? number and sizes of output, log, and temp files
* ??? perf data
* ??? module_version: str

#### `ModuleDescription`

* module_name: str
* version: str
* ??? future fields


## 6. Examples

To run the “map crop” module, it would go something roughly like this:

1. User creates file a.json:
    ```
    { "map": "WY_CO_Peach", "job": "alpha", "modules": ["map_crop"], ... }
   ```
2. User submits the run:
    ```
    $ api.py --post --url http://ta1.com/run \
    --input a.json \
    --output b.json
    ```
    The user inspects the field run_id in the file b.json to get the ID of the submitted run.
3. User queries the run status, using the run-id string:
    ```
    $ api.py --get --url http://ta1.com/run/$RUN_ID \
    --output c.json
    ```
    The file c.json contains a field named status.
4. Using the status field from step 3:
   1. If it is status is “running”, wait a minute and go back to step 3.
   2. If status is “failed”, then get the log file(s) and despair:
        ```
       $ api.py --get --url http://ta1.com/jobs/alpha/map_crop/logs --output d.zip
        ```
   3. If status is “passed”, the go on to step 5.
5. The user gets the outputs from the run:
    ```
    $ api.py --get --url http://ta1.com/jobs/alpha/map_crop/outputs \
    --output e.zip
    ```

To run all the modules, the user would do the same as above but with the module name set to “all” in step 1.
