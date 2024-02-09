#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

from __future__ import annotations

from pydantic import BaseModel
from pydantic_yaml import to_yaml_str


class TemplateParameters(BaseModel):
    disk_gb: int
    ec2_key_name: str
    instance_type: str
    owner_name: str
    region: str
    region_az: str
    stack_name: str
    ami_id: str

    def to_yaml(self) -> str:
        return to_yaml_str(self)
