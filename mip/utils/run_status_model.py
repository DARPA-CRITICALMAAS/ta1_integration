# Copyright 2024 InferLink Corporation

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from mip.utils.status_enum import StatusEnum
from mip.utils.run_payload_model import RunPayloadModel


class RunStatusModel(BaseModel):
    status: StatusEnum = StatusEnum.NOT_STARTED
    run_id: str
    payload: RunPayloadModel
    start_time: datetime
    stop_time: Optional[datetime]
    log: Optional[str]
