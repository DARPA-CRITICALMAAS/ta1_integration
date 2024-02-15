#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

from dataclasses import dataclass
import json
from glob import glob
import math
from pathlib import Path
import sys


@dataclass
class Record:
    name: str
    elapsed: int

    host_num_cpus: int
    host_total_mem: int
    host_num_gpus: int
    host_total_gpu_mem: int

    host_avg_cpu_util: float
    host_avg_mem_used: float
    host_avg_gpu_util: float
    host_avg_gpu_mem_used: float

    host_peak_cpu_util: float
    host_peak_mem_used: float
    host_peak_gpu_util: float
    host_peak_gpu_mem_used: float

    cont_num_cpus: float
    cont_total_mem: float
    cont_num_gpus: float
    cont_total_gpu_mem: float

    cont_avg_cpu_util: float
    cont_avg_mem_used: float
    cont_avg_gpu_util: float
    cont_avg_gpu_mem_used: float

    cont_peak_cpu_util: float
    cont_peak_mem_used: float
    cont_peak_gpu_util: float
    cont_peak_gpu_mem_used: float

    def headers(self) -> str:
        s = ""
        s += "name,"
        s += "elapsed,"
        s += "hhmmss,"

        s += "host_num_cpus,"
        s += "host_total_mem,"
        s += "host_num_gpus,"
        s += "host_total_gpu_mem,"

        s += "host_avg_cpu_util,"
        s += "host_avg_mem_used,"
        s += "host_avg_gpu_util,"
        s += "host_avg_gpu_mem_used,"

        s += "host_peak_cpu_util,"
        s += "host_peak_mem_used,"
        s += "host_peak_gpu_util,"
        s += "host_peak_gpu_mem_used,"

        s += "cont_num_cpus,"
        s += "cont_total_mem,"
        s += "cont_num_gpus,"
        s += "cont_total_gpu_mem,"

        s += "cont_avg_cpu_util,"
        s += "cont_avg_mem_used,"
        s += "cont_avg_gpu_util,"
        s += "cont_avg_gpu_mem_used,"

        s += "cont_peak_cpu_util,"
        s += "cont_peak_mem_used,"
        s += "cont_peak_gpu_util,"
        s += "cont_peak_gpu_mem_used,"

        s += "0\n"
        return s

    def __str__(self) -> str:
        s = ""
        s += f"{self.name},"
        s += f"{self.elapsed},"
        s += f"{time_format(self.elapsed)},"

        s += f"{self.host_num_cpus},"
        s += f"{gb(self.host_total_mem)},"
        s += f"{self.host_num_gpus},"
        s += f"{gb(self.host_total_gpu_mem)},"

        s += f"{util(self.host_avg_cpu_util)},"
        s += f"{gb(self.host_avg_mem_used)},"
        s += f"{util(self.host_avg_gpu_util)},"
        s += f"{gb(self.host_avg_gpu_mem_used)},"

        s += f"{util(self.host_peak_cpu_util)},"
        s += f"{gb(self.host_peak_mem_used)},"
        s += f"{util(self.host_peak_gpu_util)},"
        s += f"{gb(self.host_peak_gpu_mem_used)},"

        s += f"{self.cont_num_cpus},"
        s += f"{gb(self.cont_total_mem)},"
        s += f"{self.cont_num_gpus},"
        s += f"{gb(self.cont_total_gpu_mem)},"

        s += f"{util(self.cont_avg_cpu_util)},"
        s += f"{gb(self.cont_avg_mem_used)},"
        s += f"{util(self.cont_avg_gpu_util)},"
        s += f"{gb(self.cont_avg_gpu_mem_used)},"

        s += f"{util(self.cont_peak_cpu_util)},"
        s += f"{gb(self.cont_peak_mem_used)},"
        s += f"{util(self.cont_peak_gpu_util)},"
        s += f"{gb(self.cont_peak_gpu_mem_used)},"

        s += "0\n"
        return s


def time_format(secs: int) -> str:
    h = math.floor(secs / (60 * 60))
    v = secs % (60 * 60)
    m = math.floor(v / 60)
    v = v % 60
    s = v
    return f"{h:02}:{m:02}:{s:02}"


def util(x: float) -> float:
    return round(x,1)


def gb(x: float) -> float:
    return round(x / (1024*1024*1024), 1)

def json_to_record(file: str, name: str) -> Record:
    s = Path(file).read_text()
    d = json.loads(s)
    print(name)

    r = Record(
        name=name,
        elapsed = d["host"]["elapsed"],
        host_num_cpus = d["host"]["peak"]["num_cpus"],
        host_total_mem = d["host"]["peak"]["total_mem"],
        host_num_gpus = d["host"]["peak"]["num_gpus"],
        host_total_gpu_mem =  d["host"]["peak"]["total_gpu_mem"],
        host_avg_cpu_util = d["host"]["average"]["cpu_util"],
        host_avg_mem_used = d["host"]["average"]["mem_used"],
        host_avg_gpu_util = d["host"]["average"]["gpu_util"],
        host_avg_gpu_mem_used = d["host"]["average"]["gpu_mem_used"],
        host_peak_cpu_util = d["host"]["peak"]["cpu_util"],
        host_peak_mem_used = d["host"]["peak"]["mem_used"],
        host_peak_gpu_util = d["host"]["peak"]["gpu_util"],
        host_peak_gpu_mem_used = d["host"]["peak"]["gpu_mem_used"],
        cont_num_cpus = d["container"]["peak"]["num_cpus"],
        cont_total_mem = d["container"]["peak"]["total_mem"],
        cont_num_gpus = d["container"]["peak"]["num_gpus"],
        cont_total_gpu_mem =  d["container"]["peak"]["total_gpu_mem"],
        cont_avg_cpu_util = d["container"]["average"]["cpu_util"],
        cont_avg_mem_used = d["container"]["average"]["mem_used"],
        cont_avg_gpu_util = d["container"]["average"]["gpu_util"],
        cont_avg_gpu_mem_used = d["container"]["average"]["gpu_mem_used"],
        cont_peak_cpu_util = d["container"]["peak"]["cpu_util"],
        cont_peak_mem_used = d["container"]["peak"]["mem_used"],
        cont_peak_gpu_util = d["container"]["peak"]["gpu_util"],
        cont_peak_gpu_mem_used = d["container"]["peak"]["gpu_mem_used"],
    )
    return r


def main() -> int:
    d = sys.argv[1]
    files = glob(d + "/*.perf.txt")

    with open("x.csv", "w") as f:
        got_header = False
        for file in files:
            module = file[len(d)+1:-9]
            rec = json_to_record(file, module)
            if not got_header:
                print(rec.headers(), file=f)
                got_header = True
            print(rec, file=f)
    return 0


if __name__ == '__main__':
    sts = main()
    sys.exit(sts)
