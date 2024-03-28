# Copyright 2024 InferLink Corporation

from mip.utils.docker_task import DockerTask
from mip.module_tasks.legend_segment_task import LegendSegmentTask
from mip.utils.checker import check_directory_exists
from mip.module_tasks.registry import register_task


@register_task
class MapCropTask(DockerTask):
    NAME = "map_crop"
    REQUIRES = [
        LegendSegmentTask
    ]

    def run_post(self):
        d = self.task_config.host_task_output_dir

        # TODO: match this to the path/stride params
        check_directory_exists(path=d / f"{self.map_name}_g256_s256_wo_legend", min_files=1)
        check_directory_exists(path=d / f"{self.map_name}_g1000_s1000_wo_legend", min_files=1)
