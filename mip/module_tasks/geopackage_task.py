# Copyright 2024 InferLink Corporation

from mip.utils.docker_task import DockerTask
from mip.module_tasks.point_extract_task import PointExtractTask
from mip.module_tasks.line_extract_task import LineExtractTask
from mip.module_tasks.polygon_extract_task import PolygonExtractTask
from mip.module_tasks.georeference_task import GeoreferenceTask
from mip.utils.checker import check_file_exists
from mip.module_tasks.registry import register_task


@register_task
class GeopackageTask(DockerTask):
    NAME = "geopackage"
    REQUIRES = [
        PointExtractTask,
        LineExtractTask,
        PolygonExtractTask,
        GeoreferenceTask,
    ]

    def run_post(self):
        # TODO
        d = self.task_config.host_task_output_dir
