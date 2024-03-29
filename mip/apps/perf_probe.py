#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

import argparse
import sys

from mip.performance.static_info import StaticInfo
from mip.performance.dynamic_info import DynamicInfo


def get_options() -> None:
    parser = argparse.ArgumentParser()
    _args = parser.parse_args()


def main() -> int:
    get_options()

    static_info = StaticInfo.poll()
    print(static_info)

    dynamic_info = DynamicInfo.poll(static_info, elapsed=0.0)
    print(dynamic_info)

    return 0


if __name__ == '__main__':
    sys.exit(main())
