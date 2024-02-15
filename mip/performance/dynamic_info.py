# Copyright 2024 InferLink Corporation

from typing import Any

import nvidia_smi
import psutil

from mip.performance.utils import to_gb
from mip.performance.static_info import StaticInfo


class DynamicInfo:

    def __init__(self, static_info: StaticInfo):
        mem = psutil.virtual_memory()
        self.cpu_mem_used = mem.total - mem.available

        self.cpu_util = psutil.cpu_percent()

        self.gpu_mem_used = 0
        self.gpu_util = 0

        if static_info.gpu_count:
            for i in range(static_info.gpu_count):
                handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
                gpu_mem_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
                self.gpu_mem_used += gpu_mem_info.used
                gpu_util_i = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
                self.gpu_util += gpu_util_i.gpu
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "cpu_util": self.cpu_util,
            "cpu_mem_used": self.cpu_mem_used,
            "gpu_util": self.gpu_util,
            "gpu_mem_used": self.gpu_mem_used,
        }

    def __str__(self) -> str:
        s = (
            f"cpu_util={self.cpu_util}"
            + f" cpu_mem_used={to_gb(self.cpu_mem_used)}"
            + f" gpu_util={self.gpu_util}"
            + f" gpu_mem_used={to_gb(self.gpu_mem_used)}"
        )
        return s
