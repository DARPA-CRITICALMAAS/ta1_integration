# Copyright 2024 InferLink Corporation

from __future__ import annotations

from typing import Any

import nvidia_smi
import psutil
from pydantic import BaseModel

from mip.performance.utils import to_gb


# intended to be used as a singleton
class StaticInfo(BaseModel):
    cpu_count: int
    cpu_mem_total: int
    gpu_count: int
    gpu_mem_total: int

    @staticmethod
    def poll() -> StaticInfo:
        mem = psutil.virtual_memory()
        cpu_mem_total = mem.total
        cpu_count = psutil.cpu_count()

        # try:
        gpu_count = nvidia_smi.nvmlDeviceGetCount()
        # except Exception:
        #    num_gpus = 0

        gpu_mem_total = 0
        for i in range(gpu_count):
            handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
            gpu_mem_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
            gpu_mem_total += gpu_mem_info.total

        return  StaticInfo(
            cpu_count=cpu_count,
            cpu_mem_total=cpu_mem_total,
            gpu_count=gpu_count,
            gpu_mem_total=gpu_mem_total,
        )

    def __str__(self) -> str:
        s = (
            f"cpu_count={self.cpu_count}"
            + f"  cpu_mem_total={to_gb(self.cpu_mem_total)}GB"
            + f"  gpu_count={self.gpu_count}"
            + f"  gpu_mem_total={to_gb(self.gpu_mem_total)}GB"
        )
        return s
