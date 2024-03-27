# Copyright 2024 InferLink Corporation

from mip.utils.status_models import ModuleDescriptionModel
from mip.utils.configuration_models import ConfigurationModel


class MiscApi:
    def __init__(self, configuration: ConfigurationModel):
        self._module_descriptions = [
            ModuleDescriptionModel(name=i.name) for i in configuration.modules
        ]
        return

    def get_module_descriptions(self) -> list[ModuleDescriptionModel]:
        return self._module_descriptions
