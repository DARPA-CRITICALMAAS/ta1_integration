# Copyright 2024 InferLink Corporation

from typing import Any

from mip.performance.perf_event import PerfEvent


class PerfReport:
    def __init__(self):
        self._events: list[PerfEvent] = list()

    def update(self, event: PerfEvent):
        self._events.append(event)

    def _get_peak_data(self) -> PerfEvent:
        cpu_util = max([p.cpu_util for p in self._events])
        mem_used = max([p.mem_used for p in self._events])
        gpu_util = max([p.gpu_util for p in self._events])
        gpu_mem_used = max([p.gpu_mem_used for p in self._events])
        data = PerfEvent(
            elapsed=0,
            cpu_util=cpu_util,
            mem_used=mem_used,
            gpu_util=gpu_util,
            gpu_mem_used=gpu_mem_used)

        return data

    def _get_average_data(self) -> PerfEvent:
        cpu_util = sum([p.cpu_util for p in self._events]) / len(self._events)
        mem_used = round(sum([p.mem_used for p in self._events]) / len(self._events))
        gpu_util = sum([p.gpu_util for p in self._events]) / len(self._events)
        gpu_mem_used = round(sum([p.gpu_mem_used for p in self._events]) / len(self._events))
        data = PerfEvent(
            elapsed=0,
            cpu_util=cpu_util,
            mem_used=mem_used,
            gpu_util=gpu_util,
            gpu_mem_used=gpu_mem_used)

        return data

    def to_dict(self) -> dict[str, Any]:
        d = {
            "elapsed": self._events[-1].elapsed,
            "events": [e.to_dict() for e in self._events],
            "peak": self._get_peak_data().to_dict(),
            "average": self._get_average_data().to_dict(),
        }
        return d
