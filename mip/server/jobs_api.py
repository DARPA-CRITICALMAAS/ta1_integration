# Copyright 2024 InferLink Corporation

import json
from pathlib import Path
import pdb
import shutil

from mip.utils.status_models import JobStatusModel
from mip.utils.configuration_models import ConfigurationModel


class JobsApi:
    def __init__(self, configuration: ConfigurationModel):
        self._configuration = configuration
        return

    def get_jobs(self) -> list[str]:
        files = self._configuration.host.output_dir.glob("*.json")
        return [f.stem for f in files]

    def get_job_by_name(self, job_name: str) -> JobStatusModel:
        file = self._configuration.host.output_dir / f"{job_name}.json"
        data = json.loads(file.read_text())
        m = JobStatusModel(**data)
        return m
