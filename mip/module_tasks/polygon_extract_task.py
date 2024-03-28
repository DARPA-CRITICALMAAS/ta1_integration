# Copyright 2024 InferLink Corporation

from mip.utils.module_task import ModuleTask
from mip.module_tasks.legend_item_segment_task import LegendItemSegmentTask
from mip.module_tasks.legend_item_description_task import LegendItemDescriptionTask
from mip.module_tasks.registry import register_task


@register_task
class PolygonExtractTask(ModuleTask):
    NAME = "polygon_extract"
    REQUIRES = [
        LegendItemSegmentTask,
        LegendItemDescriptionTask,
    ]

    def run_post(self):
        # TODO
        pass
