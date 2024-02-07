# Copyright 2024 InferLink Corporation

from pathlib import Path

__all__ = [i.stem for i in Path(__file__).parent.glob("*_task.py")]
