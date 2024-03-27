# Copyright 2024 InferLink Corporation

from pathlib import Path

from fastapi import FastAPI, Response

from mip.utils.status_models import (
    RunPayloadModel, RunStatusModel,
    JobStatusModel,
    ModuleStatusModel, ModuleDescriptionModel,
    HelloModel,
)
from mip.server.runs_api import RunsApi
from mip.server.jobs_api import JobsApi
from mip.server.modules_api import ModulesApi
from mip.utils.configuration_models import ConfigurationModel


CONFIG_FILE = Path("config.yml")
configuration = ConfigurationModel.read(CONFIG_FILE)
runs_api = RunsApi(configuration)
jobs_api = JobsApi(configuration)
modules_api = ModulesApi(configuration)

app = FastAPI()


# ------------------------------------------------------------------------
# /HELLO
# ------------------------------------------------------------------------

@app.get("/")
async def get_hello() -> str:
    result = "Hello, mipper."
    return result


@app.post("/")
async def post_hello(body: HelloModel) -> HelloModel:
    result = HelloModel(
        greeting=body.greeting.upper(),
        name=body.name.upper(),
    )
    return result


# ------------------------------------------------------------------------
# /JOBS
# ------------------------------------------------------------------------

@app.get("/jobs/")
async def get_jobs() -> list[str]:
    result = jobs_api.get_jobs()
    return result


@app.get("/jobs/{job_name}")
async def get_job_by_name(job_name: str) -> JobStatusModel:
    result = jobs_api.get_job_by_name(job_name)
    return result


# ------------------------------------------------------------------------
# /MODULES
# ------------------------------------------------------------------------

@app.get("/modules/")
async def get_modules() -> list[ModuleDescriptionModel]:
    result = modules_api.get_module_descriptions()
    return result


@app.get("/modules/{job_name}")
async def get_module_by_job_name(job_name: str) -> list[str]:
    result = modules_api.get_modules_by_job_name(job_name)
    return result


@app.get("/modules/{job_name}/{module_name}")
async def get_module_status(job_name: str, module_name: str) -> ModuleStatusModel:
    result = modules_api.get_module_status(job_name, module_name)
    return result


@app.get("/modules/{job_name}/{module_name}/logs")
async def get_module_logs(job_name: str, module_name: str) -> Response:
    zip_file = modules_api.get_module_log_files(job_name, module_name)
    return Response(content=zip_file.read_bytes(), media_type="application/zip")


@app.get("/modules/{job_name}/{module_name}/outputs")
async def get_module_outputs(job_name: str, module_name: str) -> Response:
    zip_file = jobs_api.get_module_output_files(job_name, module_name)
    return Response(content=zip_file.read_bytes(), media_type="application/zip")


@app.get("/modules/{job_name}/{module_name}/temps")
async def get_module_temps(job_name: str, module_name: str) -> Response:
    zip_file = jobs_api.get_module_temp_files(job_name, module_name)
    return Response(content=zip_file.read_bytes(), media_type="application/zip")


# ------------------------------------------------------------------------
# /RUNS
# ------------------------------------------------------------------------

@app.post("/runs/")
async def post_run(body: RunPayloadModel) -> RunStatusModel:
    result = runs_api.start_run(body)
    return result


@app.get("/runs/")
async def get_runs() -> list[str]:
    result = runs_api.get_run_ids()
    return result


@app.get("/runs/{run_id}")
async def get_run(run_id: str) -> RunStatusModel:
    result = runs_api.get_run_status(run_id)
    return result
