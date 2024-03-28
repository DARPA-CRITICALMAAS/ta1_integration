# Copyright 2024 InferLink Corporation

from enum import Enum


class StatusEnum(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    PASSED = "PASSED"
