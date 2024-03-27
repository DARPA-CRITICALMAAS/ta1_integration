# Copyright 2024 InferLink Corporation

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as

DEFAULT_GPU = False


class ModuleConfigurationModel(BaseModel):
    name: str
    gpu: bool = DEFAULT_GPU
    options: Optional[dict[str, Union[str, int, list[int], float | bool]]] = {}


class HostConfigurationModel(BaseModel):
    input_dir: Path
    output_dir: Path
    temp_dir: Path
    repo_dir: Path
    runs_dir: Path


class ContainerConfigurationModel(BaseModel):
    input_dir: Path
    output_dir: Path
    temp_dir: Path
    repo_dir: Path


class ConfigurationModel(BaseModel):
    host: HostConfigurationModel
    container: ContainerConfigurationModel
    modules: list[ModuleConfigurationModel]

    @staticmethod
    def read(path: Path) -> ConfigurationModel:
        s = path.read_text()
        c = parse_yaml_raw_as(ConfigurationModel, s)
        return c
