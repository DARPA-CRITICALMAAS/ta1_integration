# Copyright 2024 InferLink Corporation

from __future__ import annotations
from datetime import datetime
import json
from typing import Optional

from mip.mipper.mipper_options import MipperOptions
from mip.utils.configuration_models import ConfigurationModel, ModuleConfigurationModel
from mip.utils.status_models import Status, JobStatusModel


class Context:

    # TODO: hack, because we don't know how to pass non-string state to Tasks
    CONTEXT: Optional[Context] = None

    def __init__(self, options: MipperOptions):
        Context.CONTEXT = self

        self.map_name: str = options.map_name
        self.job_name: str = options.job_name
        self.run_id: str = options.run_id

        self._configuration = ConfigurationModel.read(options.config_file)

        self.openai_key = options.openai_key_file.read_text().strip()

        self.host_input_dir = self._configuration.host.input_dir
        self.host_output_dir = self._configuration.host.output_dir
        self.host_temp_dir = self._configuration.host.temp_dir
        self.host_repo_dir = self._configuration.host.repo_dir

        self.container_input_dir = self._configuration.container.input_dir
        self.container_output_dir = self._configuration.container.output_dir
        self.container_temp_dir = self._configuration.container.temp_dir
        self.container_repo_dir = self._configuration.container.repo_dir

        self.host_job_output_dir = self.host_output_dir / self.job_name
        self.host_job_temp_dir = self.host_temp_dir / self.job_name

        self._job_status = JobStatusModel(
            job=options.job_name,
            modules=options.target_task_names,
            status=Status.RUNNING,
            start_time=datetime.now(),
            stop_time=None,
            force_rerun=options.force
        )

    def get_module_config(self, module_name: str) -> ModuleConfigurationModel:
        items = [i for i in self._configuration.modules if i.name == module_name]
        if not items:
            raise Exception(f"module not found: {module_name}")
        if len(items) > 1:
            raise Exception(f"duplicate module names found: {module_name}")
        return items[0]

    def set_exit_status(self, status: int) -> None:
        if status == 0:
            self._job_status.status = Status.PASSED
        else:
            self._job_status.status = Status.FAILED
        self._job_status.stop_time = datetime.now()

    def write_job_status(self) -> None:
        file = self.host_output_dir / f"{self.job_name}.json"
        s = self._job_status.model_dump_json(indent=4)
        file.write_text(s)
