# Copyright 2024 InferLink Corporation

import json
from pathlib import Path
import shutil

from mip.server.schemas import ModuleStatus
from mip.utils.configuration_models import ConfigurationModel


class JobsApi:
    def __init__(self, configuration: ConfigurationModel):
        self._configuration = configuration
        return

    def get_job_names(self) -> list[str]:
        files = self._configuration.host.output_dir.glob("*.json")
        return [f.stem for f in files]

    def get_module_names(self, job_name: str) -> list[str]:
        files = (self._configuration.host.output_dir / job_name).glob("*.status.json")
        return [f.stem for f in files]

    def get_module_status(self, job_name: str, module_name: str) -> ModuleStatus:
        filename = self._configuration.host.output_dir / job_name / f"{module_name}.status.json"
        data = json.loads(filename.read_text())
        run_status = ModuleStatus(**data)
        return run_status

    def get_module_log_files(self, job_name: str, module_name: str) -> Path:
        zip_file = "tmp"
        out_file = shutil.make_archive(
            base_name=zip_file,
            format="zip",
            root_dir=".",
            base_dir=self._configuration.host.log_dir / job_name / module_name)
        return Path(out_file)

    def get_module_output_files(self, job_name: str, module_name: str) -> Path:
        zip_file = "tmp"
        out_file = shutil.make_archive(
            base_name=zip_file,
            format="zip",
            root_dir=".",
            base_dir=self._configuration.host.output_dir / job_name / module_name)
        return Path(out_file)

    def get_module_temp_files(self, job_name: str, module_name: str) -> Path:
        zip_file = "tmp"
        out_file = shutil.make_archive(
            base_name=zip_file,
            format="zip",
            root_dir=".",
            base_dir=self._configuration.host.temp_dir / job_name / module_name)
        return Path(out_file)
