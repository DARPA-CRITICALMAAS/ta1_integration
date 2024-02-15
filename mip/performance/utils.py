# Copyright 2024 InferLink Corporation

import math


def to_hhmmss(secs: float | int) -> str:
    secs = float(secs)
    h = math.floor(secs / (60 * 60))
    v = secs % (60 * 60)
    m = math.floor(v / 60)
    v = v % 60
    s = v
    return f"{h:02}:{m:02}:{s:02}"


def to_utilization(x: float | int) -> int:
    return round(x)


def to_gb(x: float | int) -> int:
    x = float(x)
    gb = float(1024 ** 3)
    return round(x / gb)
