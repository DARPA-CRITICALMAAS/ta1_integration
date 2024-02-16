# Copyright 2024 InferLink Corporation

import logging
import math
import requests  # needed for docker exceptions
import time
from typing import Optional

import docker
import docker.types
import docker.errors

from mip.performance.perf_collection import PerfCollection


logger = logging.getLogger('luigi-interface')

WAIT_TIME = 10


class DockerRunner:
    def __init__(self, *,
                 name: str,
                 image: str,
                 command: list[str],
                 volumes: list[str],  # [/host:/container]
                 environment: list[str],  # [VAR=value]
                 gpus: bool,
                 user: Optional[str] = None):

        self._client = docker.from_env()

        mounts = [_make_mount(v) for v in volumes]

        if gpus:
            device = docker.types.DeviceRequest(
                driver="nvidia",
                count=-1,
                capabilities=[["gpu"]])
            devices = [device]
        else:
            devices = []

        try:
            c = self._client.containers.get(name)
            c.remove()
        except docker.errors.NotFound:
            pass

        # filter out "", used for switches with no values
        command = [c for c in command if c]

        self._container = self._client.containers.create(
            image=image,
            name=name,
            mounts=mounts,
            command=command,
            environment=environment,
            user=user,
            device_requests=devices,
        )

        vs = ""
        for v in volumes:
            vs += f" -v {v}"

        options = ""
        for c in command:
            options += f" {c}"

        gpus_s = "--gpus all" if gpus else ""
        self.shell_command = f"# docker run {gpus_s} --user {user} {vs} -it --entrypoint bash {image}\n"
        self.run_command = f"# docker run {gpus_s} --user {user} {vs} {image} {options}\n"

    # returns (status code, log data, elapsed seconds)
    def run(self, perf_collection: PerfCollection) -> tuple[int, str, int]:
        start = time.time()

        self._container.start()

        exit_status = self._wait_for_completion(perf_collection, start)

        end = time.time()
        elapsed = round(end-start)

        log = self._container.logs(stdout=True, stderr=True)
        log = log.decode("utf-8")

        return exit_status, log, elapsed

    def _wait_for_completion(self, perf_collection: PerfCollection, start_time: float) -> int:
        # use the wait(timeout) call a perf stats collector (and potential heartbeat)
        while True:
            elapsed = time.time() - start_time
            dynamic_info = perf_collection.poll(elapsed)
            s = str(dynamic_info)
            logger.info(s)

            try:
                exit_status = self._container.wait(timeout=WAIT_TIME)
                return exit_status["StatusCode"]
            except requests.exceptions.ConnectionError as ex:
                if "read timed out" in str(ex).lower():
                    pass

        # not reached


def _make_mount(v: str) -> docker.types.Mount:
    t = v.split(":")
    mount = docker.types.Mount(
        type='bind',
        source=t[0],
        target=t[1],
        read_only=False)
    return mount
