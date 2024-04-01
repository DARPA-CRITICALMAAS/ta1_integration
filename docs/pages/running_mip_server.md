# Running the Server (`mip_server`)

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

To run the server, ssh into the EC2 host and do this:

1. `cd /ta1/dev/ta1_integration`
2. `poetry shell`
3. `source env.sh`
4. `uvicorn mip.mip_server.mip_server:app`



## 4. Running the Client

The client is implemented so as not to require the full environment on the EC2
host like the other parts of the system.

1. `pip install requests`
2. `curl https://raw.githubusercontent.com/DARPA-CRITICALMAAS/ta1_integration/main/mip/mip_client/mip_client.py > mip_client.py`
3. `python ./mip_client.py [options]`

The command line options are:

* `--get`: for GET requests (required, unless `--post` is used)
* `--post`: for POST requests (required unless `--get` is used)
* `--url`: url of server (required)
* `--input`: input json file (required if `--post` is used)
* `--output`: output file (zip or JSON)

See below for examples.


## 5. The REST API

### 5.1. The "Runs" Endpoints

#### `POST /runs`

Runs the given module(s). Will also run any required predecessor modules that
haven’t yet been run.
* Payload: a RunPayload object
* Returns: a RunStatus object

#### `GET /runs`

Gets a list of all the run-ids.
* Returns: a JSON list of run-id strings

#### `GET /runs/{run-id}`

Gets the status of the given run-id.
* Returns: a RunStatus object


### 5.2. The "Jobs" API

#### `GET /jobs`

Gets a list of all jobs that have been run
* Returns: a JSON list of all the job names

#### `GET /jobs/{job_name}`

Gets info about the given job
* Returns: a JobStatusModel object


### 5.3. The "Modules" API

#### `GET /modules`

Helper function to get list of the supported modules
* Returns: list of ModuleDescription objects

#### `GET /modules/{job_name}`

Gets a list of all the modules that have been run for the given job
* Returns: a list of module names

#### `GET /modules/{job_name}/{module_name}`

Gets info about a module run under a given job name
* Returns: a ModuleStatus object

#### `GET /jobs/{job_name}/{module_name}/logs`

Gets the logs from the last run of the given job/module
* Returns: a zip file containing the log file(s)

#### `GET /jobs/{job_name}/{module_name}/outputs`

Gets the outputs from the last run of the given job/module
* Returns: a zip file containing the output file(s)

#### `GET /jobs/{job_name}/{module_name}/temps`

Gets the temp files from the last run of the given job/module
* Returns: a zip file containing the temp file(s)


### 5.4. The "Misc" API

#### `GET /maps`

Helper function to list the TIFF maps loaded onto the server
* Returns: list of map names


### 5.5. The Schemata

The following Pydantic classes (JSON dicts) are used for endpoint payloads and responses.

#### `RunPayload`

* job: str
* modules: list of str
* map: str
* force_rerun: bool _(if set, will force the module to be run, even if the
    job/module has already been successfully run)_
* openai_key: str

#### `RunStatus`

* status: enum of (not started, running, passed, failed)
* run_id: str
* payload: RunPayload
* start_time: timestamp
* stop_time: timestamp (or None, if run not finished)
* log: str (or None, if run not finished)

#### `JobStatus`

* status: enum of (not started, running, passed, failed)
* job str
* modules: list of str
* start_time: timestamp
* stop_time: timestamp (or None, if not finished)
* log: str (or None, if run not finished)
* force_rerun: bool _(reflects state of the `RunPayload.force_rerun` field)_

#### `ModuleStatus`

* status: enum of (not started, running, passed, failed)
* job str
* module: str
* start_time: timestamp
* stop_time: timestamp (or None, if not finished)
* log: str (or None, if run not finished)

#### `ModuleDescription`

* module_name: str
* version: str


## 6. Examples

Included with the system is a stand-alone tool, `mip_client.py`, to make it
easy to experiment with the server API: it allows you to perform POST or GET
operations against a given URL.

To run the "map_crop" module, it would go something roughly like this:

1. User creates file `a.json` (using the `RunPayload` schema above):
    ```
    { "map": "WY_CO_Peach", "job": "alpha", "modules": ["map_crop"], ... }
   ```
   
2. User submits the run:
    ```
    $ mip_client.py --post \
        --url http://ta1.com/runs \
        --input a.json \
        --output b.json
    ```
    The output (a `RunStatus` object) is printed to the screen and also stored
    to `b.json`. The user inspects the field `run_id` to get the ID of the
    submitted run.

3. User queries the run status, using the run-id string:
    ```
    $ mip_client.py --get 
        --url http://ta1.com/runs/$RUN_ID \
        --output c.json
    ```
    The output (to the screen and file `c.json`) follows the `RunStatus` schema
    and contains a field named `status`.

4. User queries the job status, using the job name used in step 1:
    ```
    $ mip_client.py --get 
        --url http://ta1.com/jobs/alpha \
        --output d.json
    ```
    The output (to the screen and file `d.json`) follows the `JobStatus` schema
    and contains a field named `status`.

5. Using the status field from step 3:
   1. If it is status is “running”, wait a minute and go back to step 3.
   2. If status is “failed”, then get the log file(s) and despair:
        ```
       $ mip_client.py --get 
           --url http://ta1.com/modules/alpha/map_crop/logs 
           --output d.zip
        ```
   3. If status is “passed”, the go on to step 6.

6. The user gets the outputs from the run:
    ```
    $ mip_client.py --get \
        --url http://ta1.com/modules/alpha/map_crop/outputs \
        --output e.zip
    ```
