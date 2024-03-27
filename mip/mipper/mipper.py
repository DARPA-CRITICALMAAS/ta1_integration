#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

from datetime import datetime
import os
import sys

ta1_repos_dir = os.getenv("TA1_REPOS_DIR", None)
if not ta1_repos_dir:
    print(f"$TA1_REPOS_DIR not set")
    sys.exit(1)
os.environ["LUIGI_CONFIG_PATH"] = ta1_repos_dir + "/ta1_integration/luigi.cfg"
os.environ["LUIGI_LOG_CONFIG_PATH"] = ta1_repos_dir + "/ta1_integration/luigi_log.cfg"

import luigi
import luigi.tools.deps_tree as deps_tree

from mip.module_tasks import *  # force registration of all module tasks
from mip.module_tasks.registry import registry_lookup, get_tasks
from mip.utils.context import Context
from mip.utils.module_config import ModuleConfig
from mip.utils.simple_task import SimpleTask
from mip.performance.utils import start_nvidia, shutdown_nvidia
from mip.mipper.mipper_options import MipperOptions


def main() -> int:

    start_nvidia()

    opts = MipperOptions()

    if opts.list_tasks:
        print("Registered tasks:")
        for name, cls in get_tasks().items():
            if cls.REQUIRES:
                s = ", ".join([c.NAME for c in cls.REQUIRES])
            else:
                s = "[]"
            print(f"    {name}  <--  {s}")
        return 0

    if not opts.openai_key_file.exists():
        print(f"OpenAI key file not found: {opts.openai_key_file}")
        return 1

    context = Context(opts)

    for p in [context.host_input_dir, context.host_output_dir, context.host_temp_dir]:
        if not p.exists():
            print(f"host directory not found: {p}")
            return 1
        if not p.is_dir():
            print(f"host directory is not a directory: {p}")
            return 1

    for p in [context.host_job_output_dir, context.host_job_temp_dir]:
        p.mkdir(parents=True, exist_ok=True)

    tasks: list[SimpleTask] = list()

    for task_name in opts.target_task_names:
        task_cls = registry_lookup(task_name)
        if not task_cls:
            print(f"task not found: {task_name}")
            return 1
        task = task_cls(job_name=context.job_name, map_name=context.map_name)
        tasks.append(task)

    if opts.list_deps:
        print()
        for task in tasks:
            s = f"TASK: {task.NAME} "
            print(s + "=" * (78-len(s)))
            print(deps_tree.print_tree(task))
            print("=" * 78)
            print()
        return 0

    if opts.force:
        for task_name in opts.target_task_names:
            task_config = ModuleConfig(context, task_name)
            task_config.host_task_file.unlink(missing_ok=True)

    # now we're ready to start!

    context.write_job_status()

    try:
        result = luigi.build(
            tasks=tasks,
            local_scheduler=True,
            detailed_summary=True
        )
        status = 0 if result.status == luigi.execution_summary.LuigiStatusCode.SUCCESS else 1
    except Exception:
        status = 17

    context.set_exit_status(status)

    context.write_job_status()

    shutdown_nvidia()

    return status


if __name__ == '__main__':
    sts = main()
    sys.exit(sts)
