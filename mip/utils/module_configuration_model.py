# Copyright 2024 InferLink Corporation

from typing import Optional, Union

from pydantic import BaseModel

DEFAULT_GPU = False
DEFAULT_USER = "cmaas"


class ModuleConfigurationModel(BaseModel):
    name: str
    gpu: bool = DEFAULT_GPU
    user: str = DEFAULT_USER
    options: Optional[dict[str, Union[str, int, list[int], float | bool]]] = {}
