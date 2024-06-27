# Copyright 2024 InferLink Corporation

import argparse
import os
from pathlib import Path

from mip.utils.context import create_run_id

DEFAULT_CONFIG_FILE = "./config.yml"
DEFAULT_TASK_NAME = "all"


class Options:
    def __init__(self):

        parser = argparse.ArgumentParser(
            prog="mip_job",
            description="Runs TA1 modules in an integrated fashion")

        parser.add_argument(
            "--config-file",
            type=str,
            default=DEFAULT_CONFIG_FILE,
            # help=f"path to YML configuration file (default: {DEFAULT_CONFIG_FILE})",
        )
        parser.add_argument(
            "--map-name",
            type=str,
            help="name of map (example: WY_CO_Peach)",
        )
        parser.add_argument(
            "--run-id",
            type=str,
            help="id of this run",
        )
        parser.add_argument(
            "--job-name",
            type=str,
            help="name of job to execute",
        )
        parser.add_argument(
            "--module-name",
            type=str,
            action='extend',
            nargs='*',
            help="name of target module to run (may be repeated)",
        )
        parser.add_argument(
            "--list-modules",
            action="store_true",
            help="list names of known modules and exit"
        )
        parser.add_argument(
            "--list-deps",
            action="store_true",
            help="display module dependency tree and exit"
        )
        parser.add_argument(
            "--openai-key",
            type=str,
            default=None,
            help=f"your OpenAI key string"
        )
        parser.add_argument(
            "--force-rerun",
            action="store_true",
            help="forces execution of target module, even if already completed successfully"
        )

        args = parser.parse_args()
        self.map_name: str = args.map_name
        self.run_id: str = args.run_id
        self.job_name: str = args.job_name
        self.module_names: list[str] = args.module_name
        self.config_file = Path(args.config_file)
        self.list_modules: bool = args.list_modules
        self.list_deps: bool = args.list_deps
        self.openai_key = args.openai_key
        self.force_rerun = args.force_rerun

        if self.list_modules:
            if self.map_name:
                parser.error("--map-name is not allowed with --list-modules")
            if self.module_names:
                parser.error("--module-name is not allowed with --list-modules")
            if self.job_name:
                parser.error("--job-name is not allowed with --list-modules")
            if self.run_id:
                parser.error("--run-id is not allowed with --list-modules")

        elif self.list_deps:
            if self.map_name:
                parser.error("--map-name not allowed with --list-deps")
            if not self.module_names:
                parser.error("--module-name is required with --list-deps")
            if self.job_name:
                parser.error("--job-name is not allowed with --list-deps")
            if self.run_id:
                parser.error("--run-id is not allowed with --list-deps")
            self.map_name = "NO_MAP"
            self.job_name = "NO_JOB"
            self.run_id = "NO_RUN"

        else:
            # happy path
            if not self.run_id:
                self.run_id = create_run_id()

            if not self.map_name:
                parser.error("--map-name is required")
            if not self.module_names:
                parser.error("--module-name is required")
            if not self.job_name:
                parser.error("--job-name is required")
            if not self.run_id:
                parser.error("--run-id is required")
