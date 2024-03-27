# Copyright 2024 InferLink Corporation

import json
from pathlib import Path
import pdb
from zipfile import ZipFile

from mip.utils.status_models import ModuleStatusModel, ModuleDescriptionModel
from mip.utils.configuration_models import ConfigurationModel


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
        # TODO: delete temp zip file when done
        zip_file = Path(f"{job_name}_{module_name}_logs.zip")
        files = [
            self._configuration.host.output_dir / job_name / f"{module_name}.json",
            self._configuration.host.output_dir / job_name / f"{module_name}.task",
            self._configuration.host.output_dir / job_name / f"{module_name}.docker.log",
            self._configuration.host.output_dir / job_name / module_name / "run.log",
        ]
        _make_zip(zip_file, files)
        return Path(zip_file)

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


def _make_zip(zip_file: Path, files: list[Path]) -> None:
    with ZipFile(file=zip_file, mode="w") as f:
        for file in files:
            if file.exists():
                f.write(file)
