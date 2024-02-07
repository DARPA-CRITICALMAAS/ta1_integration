# Copyright 2024 InferLink Corporation

from mip.utils.docker_task import DockerTask
from mip.module_tasks.legend_item_description_task import LegendItemDescriptionTask
from mip.module_tasks.registry import register_task


@register_task
class LineExtractTask(DockerTask):
    NAME = "line_extract"
    REQUIRES = [LegendItemDescriptionTask]

    def run_post(self):
        # TODO
        pass
