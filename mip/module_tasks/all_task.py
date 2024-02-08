# Copyright 2024 InferLink Corporation

from mip.module_tasks.registry import register_task

from mip.utils.simple_task import SimpleTask
from mip.module_tasks.geopackage_task import GeopackageTask


@register_task
class AllTask(SimpleTask):
    NAME = "all"
    REQUIRES = [
        GeopackageTask,
    ]

    def run_body(self):
        pass
