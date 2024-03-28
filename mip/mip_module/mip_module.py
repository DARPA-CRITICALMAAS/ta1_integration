#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

from datetime import datetime
import json
from pprint import pprint
import sys

from mip.module_tasks import *  # force registration of all module tasks
from mip.module_tasks.registry import get_tasks
from mip.utils.context import Context
from mip.utils.module_config import ModuleConfig
from mip.mip_module.options import Options
from mip.mip_module.module_runner import ModuleRunner


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

    if options.module_name not in get_tasks().keys():
        print(f"*** error: invalid module name: {options.module_name}")
        return 1

    if not options.openai_key_file.exists():
        print(f"*** error: OpenAI key file not found: {options.openai_key_file}")
        return 1

    context = Context(
        map_name=options.map_name,
        module_names=[options.module_name],
        job_name=options.job_name,
        run_id=options.run_id,
        force_rerun=options.force,
        config_file=options.config_file,
        openai_key_file=options.openai_key_file
    )

    status = context.verify_host_dirs()
    if status != 0:
        return status

    if options.force:
        task_config = ModuleConfig(context, options.module_name)
        task_config.host_module_luigi_file.unlink(missing_ok=True)

    status_file = context.get_module_status_filename(options.module_name)
    print(f"Status file: {status_file}")
    print(f"Started at {datetime.now()}")

    context.write_module_status(options.module_name)

    try:
        module_runner = ModuleRunner(options.module_name, context)
        status, log, elapsed = module_runner.run()

        context.set_module_state(
            module_name=options.module_name,
            stop_time=datetime.now(),
            status=status,
            log=log,
            exception=None,
        )

    except Exception as ex:
        status = 17
        elapsed = -1
        context.set_module_state(
            module_name=options.module_name,
            stop_time=datetime.now(),
            status=status,
            log=None,
            exception=ex,
        )

    context.write_module_status(options.module_name)

    print(f"Ended at {datetime.now()} ({elapsed} seconds)")
    print(f"Status: {status}")
    print("-----------------------")
    x = json.loads(status_file.read_text())
    pprint(x)
    print("-----------------------")

    return status


if __name__ == '__main__':
    sts = main()
    sys.exit(sts)
