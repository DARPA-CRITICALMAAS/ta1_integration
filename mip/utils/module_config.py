# Copyright 2024 InferLink Corporation

from __future__ import annotations

from typing import Any

from mip.utils.context import Context


class ModuleConfig:
    def __init__(self, context: Context, module_name: str):
        self._context = context
        self.task_name = module_name
        self.job_name = context.job_name

        self.container_input_dir = context.container_input_dir
        self.container_output_dir = context.container_output_dir
        self.container_temp_dir = context.container_temp_dir
        self.container_repo_dir = context.container_repo_dir

        self.container_task_output_dir = self.container_output_dir / module_name
        self.container_task_temp_dir = self.container_temp_dir / module_name

        self.host_input_dir = context.host_input_dir
        self.host_output_dir = context.host_job_output_dir
        self.host_temp_dir = context.host_job_temp_dir
        self.host_repo_dir = context.host_repo_dir

        self.host_task_output_dir = self.host_output_dir / module_name
        self.host_task_temp_dir = self.host_temp_dir / module_name

        self.host_status_file = self.host_output_dir / f"{module_name}.json"
        self.host_task_file = self.host_output_dir / f"{module_name}.task"
        self.host_docker_file = self.host_output_dir / f"{module_name}.docker.log"
        # self.host_perf_file = self.host_output_dir / f"{module_name}.perf_json"

        self._module = self._context.get_module_config(module_name)
        self.user = self._module.user
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
            s = s.replace("$MAP_NAME", self._context.map_name)
            s = s.replace("$INPUT_DIR", str(self.container_input_dir))
            s = s.replace("$OUTPUT_DIR", str(self.container_output_dir))
            s = s.replace("$TEMP_DIR", str(self.container_temp_dir))
            s = s.replace("$REPO_DIR", str(self.container_repo_dir))
            return s
        return str(s)
