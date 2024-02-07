# Copyright 2024 InferLink Corporation

from mip.utils.docker_task import DockerTask
from mip.module_tasks.legend_item_segment_task import LegendItemSegmentTask
from mip.module_tasks.registry import register_task


@register_task
class PolygonExtractTask(DockerTask):
    NAME = "polygon_extract"
    REQUIRES = [
            LegendItemSegmentTask,
        ]

    def run_post(self):
        # TODO
        pass
