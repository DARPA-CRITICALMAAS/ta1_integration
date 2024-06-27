# Copyright 2024 InferLink Corporation

from __future__ import annotations
from pathlib import Path

from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as

from mip.utils.host_configuration_model import HostConfigurationModel
from mip.utils.container_configuration_model import ContainerConfigurationModel
from mip.utils.module_configuration_model import ModuleConfigurationModel


class ConfigurationModel(BaseModel):
    host: HostConfigurationModel
    container: ContainerConfigurationModel
    modules: list[ModuleConfigurationModel]

    @staticmethod
    def read(path: Path) -> ConfigurationModel:
        s = path.read_text()

        c = parse_yaml_raw_as(ConfigurationModel, s)
        return c