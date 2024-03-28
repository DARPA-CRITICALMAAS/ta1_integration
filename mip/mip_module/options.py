# Copyright 2024 InferLink Corporation

import argparse
import os
from pathlib import Path


DEFAULT_CONFIG_FILE = "./config.yml"
DEFAULT_OPENAI_KEY_FILE = f"{os.path.expanduser('~')}/.ssh/openai"


class Options:
    def __init__(self):

        parser = argparse.ArgumentParser(
            prog="mip_modules",
            description="Runs a containerized TA1 module")

        parser.add_argument(
            "--config-file",
            type=str,
            default=DEFAULT_CONFIG_FILE,
            help=f"path to YML configuration file (default: {DEFAULT_CONFIG_FILE})",
        )
        parser.add_argument(
            "--map-name",
            type=str,
            help="name of map (example: WY_CO_Peach)",
        )
        parser.add_argument(
            "--module-name",
            type=str,
            help="name of target module to run",
        )
        parser.add_argument(
            "--job-name",
            type=str,
            help="name of job",
        )
        parser.add_argument(
            "--run-id",
            type=str,
            help="name of run",
        )
        parser.add_argument(
            "--list-modules",
            action="store_true",
            help="list names of known modules and exit"
        )
        parser.add_argument(
            "--openai_key_file",
            type=str,
            default=DEFAULT_OPENAI_KEY_FILE,
            help=f"path to file containing OpenAI key (default: {DEFAULT_OPENAI_KEY_FILE})"
        )
        parser.add_argument(
            "--force-rerun",
            action="store_true",
            help="forces execution of target module, even if already completed successfully"
        )

        args = parser.parse_args()

        self.map_name: str = args.map_name
        self.module_name = args.module_name
        self.job_name = args.job_name
        self.run_id = args.run_id
        self.config_file = Path(args.config_file)
        self.list_modules: bool = args.list_modules
        self.openai_key_file = Path(args.openai_key_file)
        self.force_rerun = args.force_rerun

        if not self.list_modules:
            if not self.map_name:
                parser.error("--map-name is required")
            if not self.module_name:
                parser.error("--module-name is required")
            if not self.job_name:
                parser.error("--job-name is required")
            if not self.run_id:
                parser.error("--run-id is required")
