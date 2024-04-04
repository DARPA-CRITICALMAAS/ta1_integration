# Copyright 2024 InferLink Corporation

from mip.utils.module_task import ModuleTask
from mip.module_tasks.legend_segment_task import LegendSegmentTask
from mip.utils.checker import check_directory_exists
from mip.module_tasks.registry import register_task


@register_task
class MapCropTask(ModuleTask):
    NAME = "map_crop"
    REQUIRES = [
        LegendSegmentTask
    ]

    def run_post(self):
        d = self.module_config.host_module_output_dir

        # match the path/stride params
        switches =  self.module_config.get_options()
        patch_switch_index = switches.index('--patch_sizes')
        stride_switch_index = switches.index('--strides')
        patches = switches[patch_switch_index+1: stride_switch_index]
        strides = switches[stride_switch_index+1: stride_switch_index+1+len(patches)]

        for i, patch in enumerate(patches):
            check_directory_exists(path=d / f"{self.map_name}_g{patch}_s{strides[i]}_wo_legend", min_files=1)

