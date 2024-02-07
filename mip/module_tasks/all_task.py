# Copyright 2024 InferLink Corporation

from mip.module_tasks.registry import register_task

from mip.utils.simple_task import SimpleTask
from mip.module_tasks.line_extract_task import LineExtractTask
from mip.module_tasks.polygon_extract_task import PolygonExtractTask
from mip.module_tasks.point_extract_task import PointExtractTask
from mip.module_tasks.georeference_task import GeoreferenceTask


@register_task
class AllTask(SimpleTask):
    NAME = "all"
    REQUIRES = [
        LineExtractTask,
        PolygonExtractTask,
        PointExtractTask,
        GeoreferenceTask,
    ]

    def run_body(self):
        pass
