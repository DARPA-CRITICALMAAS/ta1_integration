# Copyright 2024 InferLink Corporation

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from mip.performance.static_info import StaticInfo
from mip.performance.dynamic_info import DynamicInfo


class PerfCollection(BaseModel):
    elapsed: float = 0.0
    static_info: Optional[StaticInfo] = None
    dynamic_infos: list[DynamicInfo] = []

    def poll(self, elapsed: float) -> DynamicInfo:
        if not self.static_info:
            self.static_info = StaticInfo.poll()
        self.elapsed = elapsed
        d = DynamicInfo.poll(self.static_info, elapsed)
        self.dynamic_infos.append(d)
        return d

    def get_peak_data(self) -> DynamicInfo:
        cpu_util = max([p.cpu_util for p in self.dynamic_infos])
        cpu_mem_used = max([p.cpu_mem_used for p in self.dynamic_infos])
        gpu_util = max([p.gpu_util for p in self.dynamic_infos])
        gpu_mem_used = max([p.gpu_mem_used for p in self.dynamic_infos])

        d = DynamicInfo(
            elapsed=0,
            cpu_util=cpu_util,
            cpu_mem_used=cpu_mem_used,
            gpu_util=gpu_util,
            gpu_mem_used=gpu_mem_used,
        )
        return d

    def get_average_data(self) -> DynamicInfo:
        n = len(self.dynamic_infos)

        cpu_util = sum([p.cpu_util for p in self.dynamic_infos]) / n
        cpu_mem_used = sum([p.cpu_mem_used for p in self.dynamic_infos]) / n
        gpu_util = sum([p.gpu_util for p in self.dynamic_infos]) / n
        gpu_mem_used = sum([p.gpu_mem_used for p in self.dynamic_infos]) / n

        d = DynamicInfo(
            elapsed=0,
            cpu_util=round(cpu_util),
            cpu_mem_used=round(cpu_mem_used),
            gpu_util=round(gpu_util),
            gpu_mem_used=round(gpu_mem_used),
        )
        return d

    @staticmethod
    def read(path: Path) -> PerfCollection:
        with open(path) as f:
            data = json.load(f)
            obj = PerfCollection(**data)
            return obj

    def write(self, path: Path) -> None:
        with open(path, 'w') as f:
            f.write(self.model_dump_json(indent=4))

    def to_json(self) -> str:
        return self.model_dump_json(indent=4)
