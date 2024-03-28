# Copyright 2024 InferLink Corporation

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from mip.utils.status_enum import StatusEnum


class JobStatusModel(BaseModel):
    job: str
    modules: list[str]
    status: StatusEnum
    start_time: datetime
    stop_time: Optional[datetime]
    force_rerun: bool
