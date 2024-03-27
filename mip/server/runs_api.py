# Copyright 2024 InferLink Corporation
import json
from datetime import datetime
from pathlib import Path
import subprocess
from threading import Thread

from mip.utils.status_models import Status, RunPayloadModel, RunStatusModel
from mip.utils.configuration_models import ConfigurationModel


class RunsApi:
    def __init__(self, configuration: ConfigurationModel):
        self._configuration = configuration
        self._threads: list[Thread] = []
        return

    def start_run(self, body: RunPayloadModel) -> RunStatusModel:
        run_id = self._create_run_id()

        run_status = RunStatusModel(
            run_id=run_id,
            status=Status.RUNNING,
            payload=body,
            start_time=datetime.now(),
            end_time=None,
            log=None,
        )

        filename = self._get_run_id_filename(run_id)
        filename.write_text(run_status.model_dump_json())

        t = Thread(target=self._run_mipper, args=(run_status,))
        self._threads.append(t)
        t.start()
        # TODO: need to do t1.join() when done

        return run_status

    def _run_mipper(self, run_status: RunStatusModel) -> None:
        stat = subprocess.run(args=[], capture_output=True, stderr=subprocess.STDOUT, text=True)

        if stat.returncode == 0:
            run_status.status = Status.PASSED
        else:
            run_status.status = Status.FAILED

        run_status.log = stat.stdout

        run_status.payload = datetime.now()

        filename = self._get_run_id_filename(run_status.run_id)
        filename.write_text(run_status.model_dump_json())

    def get_run_ids(self) -> list[str]:
        files = self._configuration.host.runs_dir.glob("*.json")
        return [f.stem for f in files]

    def get_run_status(self, run_id: str) -> RunStatusModel:
        filename = self._get_run_id_filename(run_id)
        data = json.loads(filename.read_text())
        run_status = RunStatusModel(**data)
        return run_status

    @staticmethod
    def _create_run_id() -> str:
        s = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        return s

    def _get_run_id_filename(self, run_id: str) -> Path:
        filename = self._configuration.host.runs_dir / f"{run_id}.json"
        return filename
