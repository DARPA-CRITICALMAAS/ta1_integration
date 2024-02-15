#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

import argparse
import dataclasses
import sys
import time

import torch

from mip.performance.static_info import StaticInfo
from mip.performance.dynamic_info import DynamicInfo


@dataclasses.dataclass
class Options:
    cpu: bool
    cpu_memory: bool
    gpu: bool
    gpu_memory: bool
    duration: int


def get_options() -> Options:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cpu",
        action="store_true",
    )
    parser.add_argument(
        "--cpu-memory",
        action="store_true",
    )
    parser.add_argument(
        "--gpu",
        action="store_true",
    )
    parser.add_argument(
        "--gpu-memory",
        action="store_true",
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=15,
        help="time to run, in seconds"
    )

    args = parser.parse_args()

    options = Options(
        cpu=args.cpu,
        cpu_memory=args.cpu_memory,
        gpu=args.gpu,
        gpu_memory=args.gpu_memory,
        duration=args.duration,
    )
    return options


class ComputeLoad:
    def __init__(self, gpu: bool, memory: bool):


        if gpu:
            mem = 75 if memory else 1
            self.x = torch.linspace(0, 4, mem * 16 * 1024 ** 2).cuda()
        else:
            mem = 100 if memory else 1
            self.x = torch.linspace(0, 4, mem * 16 * 1024 ** 2)

    def work(self) -> None:
        self.x = self.x * (1.0 - self.x)


def main() -> int:
    options = get_options()

    cpu_load = None
    gpu_load = None

    print("START")

    static_info = StaticInfo()

    start = time.time()
    tick = start

    while True:
        if options.cpu:
            if not cpu_load:
                cpu_load = ComputeLoad(gpu=False, memory=options.cpu_memory)
            cpu_load.work()

        if options.gpu:
            if not gpu_load:
                gpu_load = ComputeLoad(gpu=True, memory=options.gpu_memory)
            gpu_load.work()

        now = time.time()
        if now > tick:
            dyn = DynamicInfo(static_info)
            print(dyn)
            tick = now + 1

        if (now - start) > options.duration:
            break

    print("END")

    return 0


if __name__ == '__main__':
    sys.exit(main())
