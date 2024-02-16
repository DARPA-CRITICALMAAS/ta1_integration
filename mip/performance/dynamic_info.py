# Copyright 2024 InferLink Corporation

from __future__ import annotations

from typing import Any

import nvidia_smi
import psutil

from pydantic import BaseModel

from mip.performance.utils import to_gb, to_utilization, to_hhmmss
from mip.performance.static_info import StaticInfo


class DynamicInfo(BaseModel):
    elapsed: float
    cpu_util: float
    cpu_mem_used: int
    gpu_util: float
    gpu_mem_used: int

    @staticmethod
    def poll(static_info: StaticInfo, elapsed: float) -> DynamicInfo:

        mem = psutil.virtual_memory()
        cpu_mem_used = mem.total - mem.available

        cpu_util = psutil.cpu_percent()

        gpu_mem_used = 0
        gpu_util = 0

        if static_info.gpu_count:
            for i in range(static_info.gpu_count):
                handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
                gpu_mem_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
                gpu_mem_used += gpu_mem_info.used
                gpu_util_i = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
                gpu_util += gpu_util_i.gpu

        return DynamicInfo(
            elapsed=elapsed,
            cpu_util=cpu_util,
            cpu_mem_used=cpu_mem_used,
            gpu_util=gpu_util,
            gpu_mem_used=gpu_mem_used
        )

    def __str__(self) -> str:
        s = (
            f"elapsed={to_hhmmss(self.elapsed)}"
            + f"    cpu_util={to_utilization(self.cpu_util):3}%"
            + f"    cpu_mem_used={to_gb(self.cpu_mem_used):3}GB"
            + f"    gpu_util={to_utilization(self.gpu_util):3}%"
            + f"    gpu_mem_used={to_gb(self.gpu_mem_used):3}GB"
        )
        return s
