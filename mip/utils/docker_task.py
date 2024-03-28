# Copyright 2024 InferLink Corporation

import logging
import subprocess

from mip.utils.simple_task import SimpleTask

logger = logging.getLogger('luigi-interface')


class DockerTask(SimpleTask):

    NAME = "invalid"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run_body(self):

        # self.context
        # self.task_config

        args = [
            "./mip/mip_module/mip_module.py",
            "--map-name", self.context.map_name,
            "--job-name", self.context.job_name,
            "--run-id", self.context.run_id,
            "--module-name", self.NAME,
        ]
        stat = subprocess.run(args=args, capture_output=True, text=True)  # stderr=subprocess.STDOUT

        logger.info(stat.stdout)

        if stat.returncode != 0:
            raise Exception(f"docker run failed: {self.NAME}")
