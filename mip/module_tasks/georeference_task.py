# Copyright 2024 InferLink Corporation

from mip.utils.module_task import ModuleTask
from mip.module_tasks.legend_segment_task import LegendSegmentTask
from mip.module_tasks.coordinate_spotting_task import CoordinateSpottingTask
from mip.module_tasks.registry import register_task
from mip.utils.checker import check_file_exists


@register_task
class GeoreferenceTask(ModuleTask):
    NAME = "georeference"
    REQUIRES = [
        LegendSegmentTask, 
        CoordinateSpottingTask,
        ]

    def run_post(self):
        d = self.module_config.host_module_output_dir
        check_file_exists(d / f"{self.map_name}.json", min_bytes=17)
