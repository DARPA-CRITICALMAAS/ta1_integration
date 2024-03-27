# Copyright 2024 InferLink Corporation

from __future__ import annotations

from typing import Any

from mip.utils.config import Config


class ModuleConfig:
    def __init__(self, config: Config, module_name: str):
        self._config = config
        self.task_name = module_name

        self.container_input_dir = config.container_input_dir
        self.container_output_dir = config.container_output_dir
        self.container_temp_dir = config.container_temp_dir
        self.container_repo_dir = config.container_repo_dir

        self.container_task_output_dir = self.container_output_dir / module_name
        self.container_task_temp_dir = self.container_temp_dir / module_name

        self.host_input_dir = config.host_input_dir
        self.host_output_dir = config.host_job_output_dir
        self.host_temp_dir = config.host_job_temp_dir
        self.host_repo_dir = config.host_repo_dir

        self.host_task_output_dir = self.host_output_dir / module_name
        self.host_task_temp_dir = self.host_temp_dir / module_name

        self.host_task_file = self.host_output_dir / f"{module_name}.task.txt"
        self.host_docker_file = self.host_output_dir / f"{module_name}.docker.txt"
        self.host_perf_file = self.host_output_dir / f"{module_name}.perf.json"

        self._module = self._config.get_module_config(module_name)
        self.gpu = self._module.gpu

    def get_options(self) -> list[str]:
        ret: list[str] = []
        for k, v in self._module.options.items():
            ret.append(f"--{k}")
            if type(v) is list:
                for vi in v:
                    if vi is not None:
                        ret.append(f"{self._expand(vi)}")
            else:
                if v is not None:
                    ret.append(f"{self._expand(v)}")
        return ret

    def _expand(self, s: Any) -> str:
        if type(s) is str:
            s = s.replace("$MAP_NAME", self._config.map_name)
            s = s.replace("$INPUT_DIR", str(self.container_input_dir))
            s = s.replace("$OUTPUT_DIR", str(self.container_output_dir))
            s = s.replace("$TEMP_DIR", str(self.container_temp_dir))
            s = s.replace("$REPO_DIR", str(self.container_repo_dir))
            return s
        return str(s)
