# Copyright 2024 InferLink Corporation

from mip.utils.docker_task import DockerTask
from mip.module_tasks.registry import register_task
from mip.module_tasks.start_task import StartTask
from mip.utils.checker import check_file_exists


@register_task
class GeoreferenceTask(DockerTask):
    NAME = "georeference"
    REQUIRES = [StartTask]

    def run_post(self):
        d = self.task_config.host_task_output_dir
        check_file_exists(d / f"{self.map_name}.json", min_bytes=17)
