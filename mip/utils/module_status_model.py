# Copyright 2024 InferLink Corporation

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from mip.utils.status_enum import StatusEnum


class ModuleStatusModel(BaseModel):
    status: StatusEnum
    job: str
    module: str
    start_time: datetime
    stop_time: Optional[datetime]
    exception: Optional[str]
    log: Optional[str]
