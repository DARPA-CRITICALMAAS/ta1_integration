# Copyright 2024 InferLink Corporation

import datetime
import json
import logging

from mip.utils.docker_runner import DockerRunner
from mip.utils.simple_task import SimpleTask

logger = logging.getLogger('luigi-interface')


class DockerTask(SimpleTask):

    NAME = "invalid"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run_body(self):

        docker_log_path = self.task_config.host_docker_file

        container = self._make_container()

        logger.debug("-----------------------------------------------")
        logger.debug(container.shell_command)
        logger.debug("")
        logger.debug(container.run_command)
        logger.debug("-----------------------------------------------")

        with open(docker_log_path, "w") as f:
            print(container.shell_command, file=f)
            print(container.run_command, file=f)

        status, log_data, elapsed = container.run(self.perf_collector)

        with open(docker_log_path, "a") as f:
            print(log_data, file=f)
            print("\n", file=f)

            print(f"# elapsed: {elapsed} seconds", file=f)
            print(f"# exit_status: {status}", file=f)

        logger.debug("-----------------------------------------------")
        logger.debug(log_data)
        logger.debug("-----------------------------------------------")

        s = json.dumps(self.perf_collector.to_dict(), indent=4)
        self.task_config.host_perf_file.write_text(s)

        if status:
            raise Exception(f"docker run failed: {self.NAME}")

    def _make_container(self) -> DockerRunner:
        image_name = f"inferlink/ta1_{self.NAME}"

        environment = [
            f"OPENAI_API_KEY={self.config.openai_key}"
        ]

        volumes = [
            f"{self.task_config.host_input_dir}:{self.task_config.container_input_dir}",
            f"{self.task_config.host_output_dir}:{self.task_config.container_output_dir}",
            f"{self.task_config.host_temp_dir}:{self.task_config.container_temp_dir}",
        ]

        options = self.task_config.get_options()

        container_name = f"{self.job_name}__{self.NAME}_{datetime.datetime.now().strftime('%H%M%S')}"

        container = DockerRunner(
            image=image_name,
            name=container_name,
            command=options,
            volumes=volumes,
            environment=environment,
            user=self.task_config.user,
            gpus=self.task_config.gpu,
        )

        return container
