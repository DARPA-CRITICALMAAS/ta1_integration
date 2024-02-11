# Copyright 2024 InferLink Corporation

from mip.utils.docker_task import DockerTask
from mip.module_tasks.legend_item_description_task import LegendItemDescriptionTask
from mip.module_tasks.map_crop_task import MapCropTask
from mip.utils.checker import check_directory_exists
from mip.module_tasks.registry import register_task


@register_task
class PointExtractTask(DockerTask):
    NAME = "point_extract"
    REQUIRES = [
        LegendItemDescriptionTask,
        MapCropTask,
    ]

    def run_post(self):
        # TODO
        d = self.task_config.host_task_output_dir
