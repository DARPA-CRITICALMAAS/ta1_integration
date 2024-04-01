# Copyright 2024 InferLink Corporation

from mip.utils.configuration_model import ConfigurationModel


class MiscApi:
    def __init__(self, configuration: ConfigurationModel):
        self._configuration = configuration
        return

    def get_maps(self) -> list[str]:
        files = self._configuration.host.input_dir.glob("maps/*")
        files = [f.stem for f in files]
        return sorted(files)
