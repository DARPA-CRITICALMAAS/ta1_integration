# Copyright 2024 InferLink Corporation

from __future__ import annotations

from typing import Optional

from mip.apps.options import Options
from mip.utils.configuration_models import ConfigurationModel, ModuleConfigurationModel


class Config:

    # TODO: hack, because we don't know how to pass non-string state to Tasks
    CONFIG: Optional[Config] = None

    def __init__(self, options: Options):
        self.map_name: str = options.map_name
        self.job_name: str = options.job_name

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

        Config.CONFIG = self

    def get_module_config(self, module_name: str) -> ModuleConfigurationModel:
        items = [i for i in self._configuration.modules if i.name == module_name]
        if not items:
            raise Exception(f"module not found: {module_name}")
        if len(items) > 1:
            raise Exception(f"duplicate module names found: {module_name}")
        return items[0]
