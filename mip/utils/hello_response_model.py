# Copyright 2024 InferLink Corporation

from pydantic import BaseModel


class HelloResponseModel(BaseModel):
    greeting: str
    name: str
