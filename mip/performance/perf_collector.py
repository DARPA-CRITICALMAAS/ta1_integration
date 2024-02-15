# Copyright 2024 InferLink Corporation

import time
from typing import Any, Optional

from docker.models.containers import Container
import nvidia_smi
import psutil

from mip.performance.perf_report import PerfReport
from mip.performance.perf_event import PerfEvent


class PerfCollector:

    def __init__(self):
        self._host_report = PerfReport()
        self._container_report = PerfReport()
        self._start_time = time.time()

    def update(self, container: Optional[Container] = None) -> tuple[Optional[PerfEvent], Optional[PerfEvent]]:
        host_event = self._get_host_event()
        self._host_report.update(host_event)

        if container:
            container_event = self._get_container_event(container)
            self._container_report.update(container_event)
        else:
            container_event = None

        return host_event, container_event

    def to_dict(self) -> dict[str, Any]:
        d = {
            "host": self._host_report.to_dict(),
            "container": self._container_report.to_dict(),
        }
        return d

    def _get_host_event(self) -> Optional[PerfEvent]:
        mem = psutil.virtual_memory()
        mem_bytes_used = mem.total - mem.available
        mem_bytes_total = mem.total

        cpu_perc = psutil.cpu_percent()
        num_cpus = psutil.cpu_count()

        gpu_bytes_used = 0
        gpu_bytes_total = 0
        gpu_perc = 0

        try:
            num_gpus = nvidia_smi.nvmlDeviceGetCount()
        except Exception:
            num_gpus = 0

        if num_gpus:
            for i in range(num_gpus):
                handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)

                mem_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
                gpu_bytes_used += mem_info.used
                gpu_bytes_total += mem_info.total

                gpu_util = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
                gpu_perc += gpu_util.gpu
            gpu_perc /= num_gpus

        elapsed = time.time() - self._start_time

        event = PerfEvent(
            elapsed=elapsed,
            cpu_util=cpu_perc,
            mem_used=mem_bytes_used,
            gpu_util=gpu_perc,
            gpu_mem_used=gpu_bytes_used,
            total_mem=mem_bytes_total,
            num_cpus=num_cpus,
            total_gpu_mem=gpu_bytes_total,
            num_gpus=num_gpus,
        )
        return event

    def _get_container_event(self, container: Container) -> Optional[PerfEvent]:
        stats: dict[str, Any] = container.stats(decode=False, stream=False)
        if not stats:
            return None

        # sometimes the fields are empty...
        mem_bytes_used = 0
        mem_bytes_total = 0
        num_cpus = 0.0
        cpu_perc = 0.0

        try:
            mem_bytes_used = stats["memory_stats"]["usage"]
            mem_bytes_total = stats["memory_stats"]["limit"]
            cpu_usage = (stats['cpu_stats']['cpu_usage']['total_usage']
                         - stats['precpu_stats']['cpu_usage']['total_usage'])
            cpu_system = (stats['cpu_stats']['system_cpu_usage']
                          - stats['precpu_stats']['system_cpu_usage'])
            num_cpus = stats['cpu_stats']["online_cpus"]
            cpu_perc = round((cpu_usage / cpu_system) * num_cpus * 100.0)
        except KeyError:
            pass

        elapsed = time.time() - self._start_time

        event = PerfEvent(
            elapsed=elapsed,
            cpu_util=cpu_perc,
            mem_used=mem_bytes_used,
            gpu_util=0.0,
            gpu_mem_used=0,
            total_mem=mem_bytes_total,
            num_cpus=num_cpus,
            total_gpu_mem=0,
            num_gpus=0,
        )
        return event
