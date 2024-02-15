# Copyright 2024 InferLink Corporation

from typing import Any

import nvidia_smi
import psutil

from mip.performance.utils import to_gb


class StaticInfo:

    def __init__(self):
        mem = psutil.virtual_memory()
        self.cpu_mem_total = mem.total
        self.cpu_count = psutil.cpu_count()

        # try:
        self.gpu_count = nvidia_smi.nvmlDeviceGetCount()
        # except Exception:
        #    num_gpus = 0

        self.gpu_mem_total = 0
        for i in range(self.gpu_count):
            handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
            gpu_mem_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
            self.gpu_mem_total += gpu_mem_info.total

    def to_dict(self) -> dict[str, Any]:
        return {
            "cpu_count": self.cpu_count,
            "cpu_mem_total": self.cpu_mem_total,
            "gpu_count": self.gpu_count,
            "gpu_mem_total": self.gpu_mem_total,
        }

    def __str__(self) -> str:
        s = (
            f"cpu_count={self.cpu_count}"
            + f" cpu_mem_total={to_gb(self.cpu_mem_total)}"
            + f" gpu_count={self.gpu_count}"
            + f" gpu_mem_total={to_gb(self.gpu_mem_total)}"
        )
        return s
