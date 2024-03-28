# Copyright 2024 InferLink Corporation

from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Optional

from mip.utils.configuration_models import ConfigurationModel, ModuleConfigurationModel
from mip.utils.status_models import Status, JobStatusModel, ModuleStatusModel


class Context:

    # TODO: hack, because we don't know how to pass non-string state to Tasks
    CONTEXT: Optional[Context] = None

    def __init__(
            self,
            *,
            map_name: str,
            module_names: list[str],
            job_name: str,
            run_id: str,
            force_rerun: bool,
            config_file: Path,
            openai_key_file: Path):
        Context.CONTEXT = self

        self.map_name = map_name
        self.module_names = module_names
        self.job_name = job_name
        self.run_id = run_id
        self.force_rerun = force_rerun

        self._configuration = ConfigurationModel.read(config_file)

        self.openai_key = openai_key_file.read_text().strip()

        self.host_input_dir = self._configuration.host.input_dir
        self.host_output_dir = self._configuration.host.output_dir
        self.host_temp_dir = self._configuration.host.temp_dir
        self.host_repo_dir = self._configuration.host.repo_dir
        self.host_runs_dir = self._configuration.host.runs_dir

        self.container_input_dir = self._configuration.container.input_dir
        self.container_output_dir = self._configuration.container.output_dir
        self.container_temp_dir = self._configuration.container.temp_dir
        self.container_repo_dir = self._configuration.container.repo_dir

        self.host_job_output_dir = self.host_output_dir / self.job_name
        self.host_job_temp_dir = self.host_temp_dir / self.job_name
        self.host_run_id_dir = self.host_runs_dir / self.run_id

        self._job_status = JobStatusModel(
            job=self.job_name,
            modules=self.module_names,
            status=Status.RUNNING,
            start_time=datetime.now(),
            stop_time=None,
            force_rerun=self.force_rerun
        )

        self._module_status = {
            module_name: ModuleStatusModel(
                status=Status.NOT_STARTED,
                job=self.job_name,
                module=module_name,
                start_time=datetime.now(),
                stop_time=None,
                exception=None,
                log=None,
            ) for module_name in self.module_names
        }

    def get_module_config(self, module_name: str) -> ModuleConfigurationModel:
        items = [i for i in self._configuration.modules if i.name == module_name]
        if not items:
            raise Exception(f"module not found: {module_name}")
        if len(items) > 1:
            raise Exception(f"duplicate module names found: {module_name}")
        return items[0]

    # --------------------------------------------------------------------
    # module status file
    # --------------------------------------------------------------------

    def set_module_state(
            self,
            module_name: str,
            *,
            status: Optional[int] = None,
            exception: Optional[Exception] = None,
            log: Optional[str] = None,
            stop_time: Optional[datetime] = None) -> None:

        if status is not None:
            if status == 0:
                self._module_status[module_name].status = Status.PASSED
            else:
                self._module_status[module_name].status = Status.FAILED

        if exception is not None:
            self._module_status[module_name].exception = exception

        if stop_time is not None:
            self._module_status[module_name].stop_time = stop_time

        if log is not None:
            self._module_status[module_name].log = log

    def write_module_status(self, module_name: str) -> None:
        file = self.get_module_status_filename(module_name)
        s = self._module_status[module_name].model_dump_json(indent=4)
        file.write_text(s)

    def get_module_status_filename(self, module_name: str) -> Path:
        return self.host_output_dir / self.job_name / f"{module_name}.json"

    # --------------------------------------------------------------------
    # job status
    # --------------------------------------------------------------------

    def set_job_exit_status(self, status: int) -> None:
        if status == 0:
            self._job_status.status = Status.PASSED
        else:
            self._job_status.status = Status.FAILED
        self._job_status.stop_time = datetime.now()

    def write_job_status(self) -> None:
        file = self.host_output_dir / f"{self.job_name}.json"
        s = self._job_status.model_dump_json(indent=4)
        file.write_text(s)

    # --------------------------------------------------------------------
    # dir checking
    # --------------------------------------------------------------------

    def verify_host_dirs(self) -> int:
        host_dirs = [
            self.host_input_dir,
            self.host_output_dir,
            self.host_temp_dir,
            self.host_repo_dir]

        for p in host_dirs:
            if not p.exists():
                print(f"host directory not found: {p}")
                return 1
            if not p.is_dir():
                print(f"host directory is not a directory: {p}")
                return 1

        host_dirs = [
            self.host_job_output_dir,
            self.host_job_temp_dir,
            self.host_run_id_dir]
        for p in host_dirs:
            p.mkdir(parents=True, exist_ok=True)

        return 0
