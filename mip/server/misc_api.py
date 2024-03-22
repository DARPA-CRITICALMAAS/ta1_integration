# Copyright 2024 InferLink Corporation

from mip.server.schemas import ModuleDescription
from mip.utils.configuration_models import ConfigurationModel


class MiscApi:
    def __init__(self, configuration: ConfigurationModel):
        self._module_descriptions = [
            ModuleDescription(name=i.name) for i in configuration.modules
        ]
        return

    def get_module_descriptions(self) -> list[ModuleDescription]:
        return self._module_descriptions
