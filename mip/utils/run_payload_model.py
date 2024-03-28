# Copyright 2024 InferLink Corporation

from typing import Optional

from pydantic import BaseModel


class RunPayloadModel(BaseModel):
    job: str
    modules: list[str]
    map: str
    force_rerun: bool
    openai_key: str
