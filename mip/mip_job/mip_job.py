#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

from datetime import datetime
import json
import os
from pprint import pprint
import sys

# Get the absolute path of the current directory
# current_directory = os.path.abspath(os.path.dirname(__file__))

# Add the current directory to sys.path

ta1_repos_dir = os.getenv("TA1_REPOS_DIR", None)
if not ta1_repos_dir:
    print(f"$TA1_REPOS_DIR not set")
    sys.exit(1)
sys.path.append(f'{ta1_repos_dir}/ta1_integration')

os.environ["LUIGI_CONFIG_PATH"] = ta1_repos_dir + "/ta1_integration/luigi.cfg"
os.environ["LUIGI_LOG_CONFIG_PATH"] = ta1_repos_dir + "/ta1_integration/luigi_log.cfg"

import luigi
import luigi.tools.deps_tree as deps_tree

from mip.module_tasks import *  # force registration of all module tasks
from mip.module_tasks.registry import registry_lookup, get_tasks
from mip.utils.context import Context
from mip.utils.module_config import ModuleConfig
from mip.utils.simple_task import SimpleTask
from mip.mip_job.options import Options


def main() -> int:

    options = Options()

    if options.list_modules:
        print("Registered modules:")
        for name, cls in get_tasks().items():
            if cls.REQUIRES:
                s = ", ".join([c.NAME for c in cls.REQUIRES])
            else:
                s = "[]"
            print(f"    {name}  <--  {s}")
        return 0

    context = Context(
        map_name=options.map_name,
        module_names=options.module_names,
        job_name=options.job_name,
        run_id=options.run_id,
        force_rerun=options.force_rerun,
        config_file=options.config_file,
        openai_key=options.openai_key
    )

    context.verify_host_dirs()

    tasks: list[SimpleTask] = list()

    for module_name in options.module_names:
        task_cls = registry_lookup(module_name)
        if not task_cls:
            print(f"task not found: {module_name}")
            return 1
        task = task_cls(job_name=context.job_name, map_name=context.map_name)
        tasks.append(task)

    if options.list_deps:
        print()
        for task in tasks:
            s = f"TASK: {task.NAME} "
            print(s + "=" * (78-len(s)))
            print(deps_tree.print_tree(task))
            print("=" * 78)
            print()
        return 0

    if options.force_rerun:
        for module_name in options.module_names:
            task_config = ModuleConfig(context, module_name)
            task_config.host_module_luigi_file.unlink(missing_ok=True)

    # now we're ready to start!

    start_time = datetime.now()

    status_file = context.get_job_status_filename()
    print(f"Status file: {status_file}")
    print(f"Started at {datetime.now()}")

    context.write_job_status()

    try:
        result = luigi.build(
            tasks=tasks,
            local_scheduler=True,
            detailed_summary=True
        )
        status = 0 if result.status == luigi.execution_summary.LuigiStatusCode.SUCCESS else 1

        context.set_job_state(
            status=status,
            stop_time=datetime.now(),
        )

    except Exception as ex:
        status = 17

    context.set_job_state(
        status=status,
        stop_time=datetime.now(),
    )

    context.write_job_status()

    elapsed = int((datetime.now() - start_time).total_seconds())

    print(f"Ended at {datetime.now()} ({elapsed} seconds)")
    print(f"Status: {status}")
    print("-----------------------")
    x = json.loads(status_file.read_text())
    print("-----------------------")

    return status


if __name__ == '__main__':
    sts = main()
    sys.exit(sts)
