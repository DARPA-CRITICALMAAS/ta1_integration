# Copyright 2024 InferLink Corporation

from datetime import datetime
import os
import sys

from mip.utils.context import Context
from mip.utils.module_config import ModuleConfig
from mip.utils.docker_runner import DockerRunner


class ModuleRunner:

    def __init__(self, module_name: str, context: Context):
        self._module_config = ModuleConfig(context, module_name)

        image_name = f"inferlink/ta1_{module_name}"

        environment = [
            f"OPENAI_API_KEY={context.openai_key}"
        ]

        volumes = [
            f"{self._module_config.host_input_dir}:{self._module_config.container_input_dir}",
            f"{self._module_config.host_output_dir}:{self._module_config.container_output_dir}",
            f"{self._module_config.host_temp_dir}:{self._module_config.container_temp_dir}",
        ]

        options = self._module_config.get_options()

        container_name = f"{module_name}_{datetime.now().strftime('%H%M%S')}"

        self._docker_runner = DockerRunner(
            image=image_name,
            name=container_name,
            command=options,
            volumes=volumes,
            environment=environment,
            user=self._module_config.user,
            gpus=self._module_config.gpu,
        )

    # returns (status code, log data, elapsed seconds)
    def run(self) -> tuple[int, str, int]:
        status, log_data, elapsed = self._docker_runner.run()
        return status, log_data, elapsed
