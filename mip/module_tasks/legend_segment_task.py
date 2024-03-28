# Copyright 2024 InferLink Corporation

from mip.utils.module_task import ModuleTask
from mip.utils.checker import check_file_exists
from mip.module_tasks.registry import register_task


@register_task
class LegendSegmentTask(ModuleTask):
    NAME = "legend_segment"
    REQUIRES = []

    def run_post(self):
        d = self.module_config.host_module_output_dir / f"{self.map_name}_map_segmentation.json"
        check_file_exists(d)
