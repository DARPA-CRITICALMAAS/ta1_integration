# Copyright 2024 InferLink Corporation

from mip.utils.module_task import ModuleTask
from mip.module_tasks.map_crop_task import MapCropTask
from mip.utils.checker import check_directory_exists
from mip.module_tasks.registry import register_task


@register_task
class TextSpottingTask(ModuleTask):
    NAME = "text_spotting"
    REQUIRES = [MapCropTask]

    # USER = "root"
    GPU = True

    def run_post(self):
        pass
        # d = self.module_config.host_module_output_dir
        # check_directory_exists(d / "mapKurator_test" / "spotter" / "test")