# Copyright 2024 InferLink Corporation

from datetime import datetime
try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum
from typing import Optional

from pydantic import BaseModel


class Status(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    PASSED = "PASSED"


class RunPayload(BaseModel):
    job: str
    modules: list[str]
    map: str
    force_rerun: Optional[bool] = False
    module_options: Optional[dict[str, str]] = dict()


class RunStatus(BaseModel):
    status: Status
    run_id: str
    payload: RunPayload
    start_time: datetime
    stop_time: Optional[datetime] = None
    log: Optional[str] = None


class ModuleStatus(BaseModel):
    status: Status
    job: str
    module: str
    start_time: datetime
    stop_time: Optional[datetime] = None


class ModuleDescription(BaseModel):
    name: str
    version: Optional[str] = None


class HelloModel(BaseModel):
    greeting: str
    name: str
