# Copyright 2024 InferLink Corporation

from mip.module_tasks.registry import register_task
from mip.utils.module_task import ModuleTask
from mip.module_tasks.legend_segment_task import LegendSegmentTask
from mip.module_tasks.legend_item_segment_task import LegendItemSegmentTask
from mip.utils.checker import check_file_exists


@register_task
class LegendItemDescriptionTask(ModuleTask):
    NAME = "legend_item_description"
    REQUIRES = [
        LegendSegmentTask,
        LegendItemSegmentTask,
    ]

    def run_pre(self):
        d = self.module_config.host_module_temp_dir

        # TODO: still needed?
        (d / "gpt4_input_dir").mkdir(parents=True, exist_ok=True)
        (d / "gpt4_temp_dir").mkdir(parents=True, exist_ok=True)

    def run_post(self):
        d = self.module_config.host_module_output_dir
        check_file_exists(d / f"{self.map_name}_point.json")
        check_file_exists(d / f"{self.map_name}_line.json")
        check_file_exists(d / f"{self.map_name}_polygon.json")
