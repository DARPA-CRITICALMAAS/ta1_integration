# Copyright 2024 InferLink Corporation

from typing import Optional

from pydantic import BaseModel


class ModuleDescriptionModel(BaseModel):
    name: str
    version: Optional[str] = None
