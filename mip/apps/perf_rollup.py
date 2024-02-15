#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

from glob import glob
from pathlib import Path
import sys

from mip.performance.perf_collection import PerfCollection
from mip.performance.utils import to_utilization, to_hhmmss, to_gb

def csv_header() -> str:
    s = ""
    s += "name,"
    s += "elapsed sec,"
    s += "hhmmss,"

    s += "cpu_count,"
    s += "cpu_mem_total GB,"
    s += "gpu_count,"
    s += "gpu_mem_total GB,"

    s += "avg_cpu_util %,"
    s += "avg_cpu_mem_used GB,"
    s += "avg_gpu_util %,"
    s += "avg_gpu_mem_used GB,"

    s += "peak_cpu_util %,"
    s += "peak_cpu_mem_used GB,"
    s += "peak_gpu_util %,"
    s += "peak_gpu_mem_used GB"

    return s


def csv_record(collection: PerfCollection, module_name: str) -> str:
    s = ""
    s += f"{module_name},"
    s += f"{collection.elapsed},"
    s += f"{to_hhmmss(collection.elapsed)},"

    s += f"{collection.static_info.cpu_count},"
    s += f"{to_gb(collection.static_info.cpu_mem_total)},"
    s += f"{collection.static_info.gpu_count},"
    s += f"{to_gb(collection.static_info.gpu_mem_total)},"

    avg = collection.get_average_data()
    s += f"{to_utilization(avg.cpu_util)},"
    s += f"{to_gb(avg.cpu_mem_used)},"
    s += f"{to_utilization(avg.gpu_util)},"
    s += f"{to_gb(avg.gpu_mem_used)},"

    peak = collection.get_peak_data()
    s += f"{to_utilization(peak.cpu_util)},"
    s += f"{to_gb(peak.cpu_mem_used)},"
    s += f"{to_utilization(peak.gpu_util)},"
    s += f"{to_gb(peak.gpu_mem_used)},"

    return s


def main() -> int:
    output_dir = sys.argv[1]
    files = glob(output_dir + "/*.perf.json")

    rollup_file = output_dir + "/rollup.csv"
    with open(rollup_file, "w") as f:
        got_header = False
        for file in files:
            module_name = file[len(output_dir)+1:-9]

            collection = PerfCollection.read(Path(file))
            rec = csv_record(collection, module_name)
            if not got_header:
                print(csv_header(), file=f)
                got_header = True
            print(rec, file=f)
    return 0


if __name__ == '__main__':
    sts = main()
    sys.exit(sts)
