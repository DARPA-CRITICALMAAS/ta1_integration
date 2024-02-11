# Copyright 2024 InferLink Corporation

from mip.utils.simple_task import SimpleTask
from mip.utils.checker import check_file_exists
from mip.module_tasks.registry import register_task
from mip.module_tasks.registry import register_task


@register_task
class StartTask(SimpleTask):
    NAME = "start"
    REQUIRES = []

    def run_pre(self):
        check_file_exists(
            self.task_config.host_input_dir
            / "maps"
            / self.config.map_name
            / f"{self.config.map_name}.tif")

    def run_body(self):
        (self.task_config.host_task_output_dir / "output.txt").write_text("ok\n")
        (self.task_config.host_task_temp_dir / "temp.txt").write_text("ok\n")

    def run_post(self):
        check_file_exists(self.task_config.host_task_output_dir / "output.txt", 2)
        check_file_exists(self.task_config.host_task_temp_dir / "temp.txt", 2)
