# Copyright 2024 InferLink Corporation

from mip.utils.module_task import ModuleTask
from mip.module_tasks.ptln_legend_item_description_task import PtlnLegendItemDescriptionTask
from mip.module_tasks.map_crop_task import MapCropTask
from mip.module_tasks.registry import register_task


@register_task
class PointExtractTask(ModuleTask):
    NAME = "point_extract"
    REQUIRES = [
        PtlnLegendItemDescriptionTask,
        MapCropTask,
    ]

    def run_post(self):
        # TODO
        pass
