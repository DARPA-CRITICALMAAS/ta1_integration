# Copyright 2024 InferLink Corporation

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Status(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    PASSED = "PASSED"


class RunPayloadModel(BaseModel):
    job: str
    modules: list[str]
    map: str
    force_rerun: Optional[bool] = False


class RunStatusModel(BaseModel):
    status: Status = Status.NOT_STARTED
    run_id: str
    payload: RunPayloadModel
    start_time: datetime
    stop_time: Optional[datetime] = None
    log: Optional[str] = None


class JobStatusModel(BaseModel):
    job: str
    modules: list[str]
    status: Status
    start_time: datetime
    stop_time: Optional[datetime] = None
    force_rerun: bool


class ModuleStatusModel(BaseModel):
    status: Status
    job: str
    module: str
    start_time: datetime
    stop_time: Optional[datetime] = None
    exception: Optional[str]


class ModuleDescriptionModel(BaseModel):
    name: str
    version: Optional[str] = None


class HelloModel(BaseModel):
    greeting: str
    name: str
