# Copyright 2024 InferLink Corporation

import json
import os
from pathlib import Path
import shutil
import tempfile

from mip.utils.module_status_model import ModuleStatusModel
from mip.utils.module_description_model import ModuleDescriptionModel
from mip.utils.configuration_model import ConfigurationModel


class ModulesApi:
    def __init__(self, configuration: ConfigurationModel):
        self._configuration = configuration

        self._module_descriptions = [
            ModuleDescriptionModel(name=i.name) for i in configuration.modules
        ]
        return

    def get_module_descriptions(self) -> list[ModuleDescriptionModel]:
        return self._module_descriptions

    def get_modules_by_job_name(self, job_name: str) -> list[str]:
        files = (self._configuration.host.output_dir / job_name).glob("*.json")
        return [f.stem for f in files]

    def get_module_status(self, job_name: str, module_name: str) -> ModuleStatusModel:
        filename = self._configuration.host.output_dir / job_name / f"{module_name}.json"
        data = json.loads(filename.read_text())
        run_status = ModuleStatusModel(**data)
        return run_status

    def get_module_log_files(self, job_name: str, module_name: str) -> Path:
        base_name = f"{job_name}_{module_name}_logs"
        files = [
            self._configuration.host.output_dir / job_name / f"{module_name}.json",
            self._configuration.host.output_dir / job_name / f"{module_name}.task",
            self._configuration.host.output_dir / job_name / f"{module_name}.docker.log",
            self._configuration.host.output_dir / job_name / module_name / "run.log",
        ]
        return _make_zip_from_files(base_name, files)

    def get_module_output_files(self, job_name: str, module_name: str) -> Path:
        base_name = f"{job_name}_{module_name}_outputs"
        source_dir = self._configuration.host.output_dir / job_name / module_name
        return _make_zip_from_dir(base_name, source_dir)

    def get_module_temp_files(self, job_name: str, module_name: str) -> Path:
        base_name = f"{job_name}_{module_name}_temps"
        source_dir = self._configuration.host.temp_dir / job_name / module_name
        return _make_zip_from_dir(base_name, source_dir)


def _make_zip_from_files(name: str, files: list[Path]) -> Path:
    work_dir = tempfile.mkdtemp()  # TODO: delete me!
    base_filename = f"{work_dir}/{name}"

    sources_dir = f"{work_dir}/{name}"
    os.makedirs(sources_dir, exist_ok=True)

    for file in files:
        # we skip any files that don't exist
        if file.exists():
            if not file.is_file():
                raise ValueError(f"source is not a file: {file}")
            shutil.copy(file, sources_dir)

    actual_zip_filename = shutil.make_archive(
        base_name=base_filename,
        format="zip",
        root_dir=work_dir,
        base_dir=name)

    return Path(actual_zip_filename)


def _make_zip_from_dir(name: str, directory: Path) -> Path:
    work_dir = tempfile.mkdtemp()  # TODO: delete me!
    base_filename = f"{work_dir}/{name}"

    sources_dir = f"{work_dir}/{name}"

    if not directory.exists() or not directory.is_dir():
        raise ValueError(f"source is not a directory: {directory}")
    shutil.copytree(directory, sources_dir)

    actual_zip_filename = shutil.make_archive(
        base_name=base_filename,
        format="zip",
        root_dir=work_dir,
        base_dir=name)

    return Path(actual_zip_filename)
