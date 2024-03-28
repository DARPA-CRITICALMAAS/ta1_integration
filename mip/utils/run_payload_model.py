# Copyright 2024 InferLink Corporation

from pydantic import BaseModel


class RunPayloadModel(BaseModel):
    job: str
    modules: list[str]
    map: str
    force_rerun: bool
