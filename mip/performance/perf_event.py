# Copyright 2024 InferLink Corporation

from typing import Any


# utilization is in percent, [0...n*100]
# memory is in bytes
class PerfEvent:

    def __init__(
            self,
            *,
            elapsed: float,
            cpu_util: float,  # percentage, [0..n*100]
            mem_used: int,  # bytes
            gpu_util: float,  # percentage, [0..n*100]
            gpu_mem_used: int,
            num_cpus: int = 0,
            total_mem: int = 0,
            num_gpus: int = 0,
            total_gpu_mem: int = 0,
    ):
        self.elapsed = round(elapsed)

        self.cpu_util = cpu_util
        self.mem_used = mem_used
        self.gpu_util = gpu_util
        self.gpu_mem_used = gpu_mem_used

        self.num_cpus = num_cpus
        self.total_mem = total_mem
        self.num_gpus = num_gpus
        self.total_gpu_mem = total_gpu_mem

    def to_dict(self) -> dict[str, Any]:

        return {
            "elapsed": self.elapsed,
            "cpu_util": self.cpu_util,
            "mem_used": self.mem_used,
            "gpu_util": self.gpu_util,
            "gpu_mem_used": self.gpu_mem_used,
            "num_cpus": self.num_cpus,
            "total_mem": self.total_mem,
            "num_gpus": self.num_gpus,
            "total_gpu_mem": self.total_gpu_mem,
        }
