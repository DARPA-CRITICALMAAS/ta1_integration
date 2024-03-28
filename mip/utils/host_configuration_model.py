# Copyright 2024 InferLink Corporation

from pathlib import Path

from pydantic import BaseModel


class HostConfigurationModel(BaseModel):
    input_dir: Path
    output_dir: Path
    temp_dir: Path
    repo_dir: Path
    runs_dir: Path
