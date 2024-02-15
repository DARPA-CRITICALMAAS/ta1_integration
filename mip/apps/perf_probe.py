#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

import argparse
import sys

import nvidia_smi

from mip.performance.static_info import StaticInfo
from mip.performance.dynamic_info import DynamicInfo


def get_options() -> None:
    parser = argparse.ArgumentParser()
    _args = parser.parse_args()


def main() -> int:
    get_options()

    nvidia_smi.nvmlInit()

    static_info = StaticInfo()
    print(static_info)

    dynamic_info = DynamicInfo(static_info)
    print(dynamic_info)

    nvidia_smi.nvmlShutdown()

    return 0


if __name__ == '__main__':
    sys.exit(main())
