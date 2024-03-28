# Copyright 2024 InferLink Corporation

from mip.utils.module_task import ModuleTask
from mip.module_tasks.legend_segment_task import LegendSegmentTask
from mip.module_tasks.point_extract_task import PointExtractTask
from mip.module_tasks.line_extract_task import LineExtractTask
from mip.module_tasks.polygon_extract_task import PolygonExtractTask
from mip.module_tasks.georeference_task import GeoreferenceTask
from mip.module_tasks.registry import register_task


@register_task
class GeopackageTask(ModuleTask):
    NAME = "geopackage"
    REQUIRES = [
        LegendSegmentTask,
        PointExtractTask,
        LineExtractTask,
        PolygonExtractTask,
        GeoreferenceTask,
    ]

    def run_post(self):
        # TODO
        d = self.module_config.host_module_output_dir
