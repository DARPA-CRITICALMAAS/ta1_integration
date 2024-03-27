# Copyright 2024 InferLink Corporation

from __future__ import annotations

from datetime import datetime
import logging
import shutil
from typing import Optional

import luigi

from mip.utils.context import Context
from mip.utils.module_config import ModuleConfig
from mip.performance.perf_collection import PerfCollection
from mip.utils.status_models import ModuleStatusModel, Status


logger = logging.getLogger('luigi-interface')


class SimpleTask(luigi.Task):
    NAME = "__simple__"
    REQUIRES: list[type[SimpleTask]] = None

    job_name = luigi.Parameter()
    map_name = luigi.Parameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context = Context.CONTEXT
        self.task_config = ModuleConfig(self.context, self.NAME)
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

        self.perf_collection = PerfCollection()

        self._status_object: Optional[ModuleStatusModel] = None

    def _make_status_object(self) -> None:
        self._status_object = ModuleStatusModel(
            status=Status.RUNNING,
            job=self.task_config.job_name,
            module=self.task_config.task_name,
            start_time=datetime.now(),
            stop_time=None,
            exception=None,
        )
        s = self._status_object.model_dump_json(indent=4)
        self.task_config.host_status_file.write_text(s)
        
    def _write_status_object(self, ex: Optional[Exception] = None) -> None:
        self._status_object.stop_time = datetime.now()

        if ex:
            self._status_object.exception = ex
            self._status_object.status = Status.FAILED
        else:
            self._status_object.status = Status.PASSED

        s = self._status_object.model_dump_json(indent=4)
        self.task_config.host_status_file.write_text(s)

    def run(self):
        self.start_time = datetime.now()

        self._make_status_object()

        for p in [self.task_config.host_task_output_dir, self.task_config.host_task_temp_dir]:
            if p.exists():
                shutil.rmtree(p)
            p.mkdir(parents=False, exist_ok=False)

        try:
            self.run_pre()
        except Exception as ex:
            logger.error(f"FAIL: run_pre() of {self.task_config.task_name}")
            self._write_status_object(ex)
            raise

        logger.info(f"run_pre() completed: {self.task_config.task_name}")

        try:
            self.run_body()
        except Exception as ex:
            logger.error(f"FAIL: run_body() of {self.task_config.task_name}")
            self._write_status_object(ex)
            raise

        logger.info(f"run_body() completed: {self.task_config.task_name}")

        try:
            self.run_post()
        except Exception as ex:
            logger.error(f"FAIL: run_post() of {self.task_config.task_name}")
            self._write_status_object(ex)
            raise

        logger.info(f"run_post() completed: {self.task_config.task_name}")

        self.end_time = datetime.now()
        elapsed = round((self.end_time-self.start_time).total_seconds())

        logger.info("-----------------------------------------------")
        logger.info(f"task: {self.task_config.task_name}")
        logger.info(f"elapsed: {elapsed} secs")
        logger.info("-----------------------------------------------")

        self._write_status_object()

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
        return luigi.LocalTarget(self.task_config.host_task_file)

    def requires(self):
        # force each class to list their predecessors
        assert self.REQUIRES is not None

        return [
            cls(job_name=self.context.job_name, map_name=self.context.map_name)
            for cls in self.REQUIRES
        ]
