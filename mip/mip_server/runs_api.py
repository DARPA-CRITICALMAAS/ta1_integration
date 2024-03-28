# Copyright 2024 InferLink Corporation

from datetime import datetime
import json
from pathlib import Path
import subprocess
from threading import Thread

from mip.utils.status_enum import StatusEnum
from mip.utils.run_payload_model import RunPayloadModel
from mip.utils.run_status_model import RunStatusModel
from mip.utils.configuration_model import ConfigurationModel


class RunsApi:
    def __init__(self, configuration: ConfigurationModel):
        self._configuration = configuration
        self._threads: list[Thread] = []
        return

    def post_run(self, body: RunPayloadModel) -> RunStatusModel:
        run_id = self._create_run_id()

        filename = self._get_run_id_filename(run_id)
        if filename.exists():
            # TODO: don't run more than once a second...
            raise NotImplementedError("too many runs at the same time")

        run_status = RunStatusModel(
            run_id=run_id,
            status=StatusEnum.RUNNING,
            payload=body,
            start_time=datetime.now(),
            stop_time=None,
            end_time=None,
            log=None,
        )
        filename.write_text(run_status.model_dump_json())

        t = Thread(target=self._run_mipper, args=(run_status,))
        self._threads.append(t)
        t.start()
        # TODO: need to do t1.join() when done

        return run_status

    def _run_mipper(self, run_status: RunStatusModel) -> None:
        args = [
            "./mip/mip_job/mip_job.py",
            "--map-name", run_status.payload.map,
            "--job-name", run_status.payload.job,
            "--run-id", run_status.run_id,
            ]
        if run_status.payload.force_rerun:
            args.append("--force-rerun")
        for module_name in run_status.payload.modules:
            args.append("--module-name")
            args.append(module_name)

        print("===" + " ".join(args))

        stat = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        if stat.returncode == 0:
            run_status.status = StatusEnum.PASSED
        else:
            run_status.status = StatusEnum.FAILED

        run_status.log = stat.stdout

        run_status.stop_time = datetime.now()

        filename = self._get_run_id_filename(run_status.run_id)
        filename.write_text(run_status.model_dump_json())

    def get_runs(self) -> list[str]:
        files = self._configuration.host.runs_dir.glob("*.json")
        files = [f.stem for f in files]
        return sorted(files)

    def get_run_by_name(self, run_id: str) -> RunStatusModel:
        filename = self._get_run_id_filename(run_id)
        data = json.loads(filename.read_text())
        run_status = RunStatusModel(**data)
        return run_status

    @staticmethod
    def _create_run_id() -> str:
        s = datetime.now().strftime("%Y%m%d-%H%M%S")
        return s

    def _get_run_id_filename(self, run_id: str) -> Path:
        filename = self._configuration.host.runs_dir / f"{run_id}.json"
        return filename
