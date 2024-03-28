# Copyright 2024 InferLink Corporation

from __future__ import annotations
from datetime import datetime
import logging
import shutil
from typing import Optional

import luigi

from mip.utils.context import Context
from mip.utils.module_config import ModuleConfig


logger = logging.getLogger('luigi-interface')


class SimpleTask(luigi.Task):
    NAME = "__simple__"
    REQUIRES: list[type[SimpleTask]] = None

    job_name = luigi.Parameter()
    map_name = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context = Context.CONTEXT
        self.module_config = ModuleConfig(self.context, self.NAME)
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def run(self):
        self.start_time = datetime.now()

        for p in [self.module_config.host_module_output_dir, self.module_config.host_module_temp_dir]:
            if p.exists():
                shutil.rmtree(p)
            p.mkdir(parents=False, exist_ok=False)

        try:
            self.run_pre()
        except Exception as ex:
            logger.error(f"FAIL: run_pre() of {self.module_config.module_name}")
            raise

        logger.info(f"run_pre() completed: {self.module_config.module_name}")

        try:
            self.run_body()
        except Exception as ex:
            logger.error(f"FAIL: run_body() of {self.module_config.module_name}")
            raise

        logger.info(f"run_body() completed: {self.module_config.module_name}")

        try:
            self.run_post()
        except Exception as ex:
            logger.error(f"FAIL: run_post() of {self.module_config.module_name}")
            raise

        logger.info(f"run_post() completed: {self.module_config.module_name}")

        self.end_time = datetime.now()
        elapsed = round((self.end_time-self.start_time).total_seconds())

        logger.info("-----------------------------------------------")
        logger.info(f"task: {self.module_config.module_name}")
        logger.info(f"elapsed: {elapsed} secs")
        logger.info("-----------------------------------------------")

        with self.output().open('w') as f:
            f.write(f"job_name: {self.job_name}\n")
            f.write(f"map_name: {self.map_name}\n")
            f.write(f"start_time: {self.start_time}\n")
            f.write(f"end_time: {self.end_time}\n")
            elapsed = round((self.end_time - self.start_time).total_seconds())
            f.write(f"elapsed: {elapsed} seconds\n")

    def run_pre(self):
        pass

    # override this
    def run_body(self):
        raise NotImplementedError()

    def run_post(self):
        pass

    def output(self):
        return luigi.LocalTarget(self.module_config.host_module_luigi_file)

    def requires(self):
        # force each class to list their predecessors
        assert self.REQUIRES is not None

        return [
            cls(job_name=self.context.job_name, map_name=self.context.map_name)
            for cls in self.REQUIRES
        ]
