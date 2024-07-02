#!/usr/bin/env python
# Copyright 2024 InferLink Corporation

import json
from pathlib import Path
import random
import sys
from time import sleep
from typing import Optional
import os
from filelock import FileLock
from flask import Flask, request, abort, current_app
import hmac
from mip.mip_server.modules_api import ModulesApi
from mip.mip_server.runs_api import RunsApi
from mip.utils.configuration_model import ConfigurationModel
from mip.utils.process_georef_output_cdr import georef4CDR
from mip.utils.process_feature_output_cdr import feature4CDR
from cdr_schemas.georeference import GeoreferenceResults
from cdr_schemas.feature_results import FeatureResults
import asyncio
import httpx
import time

app = Flask(__name__)
app.config["name"] = os.getenv("SYSTEM_NAME")
app.config["version"] = os.getenv("SYSTEM_VERSION")
app.config["cdr_token"] = os.getenv("CDR_TOKEN")
app.config["callback_url"] = os.getenv("CALLBACK_URL")
app.config["callback_secret"] = os.getenv("CALLBACK_SECRET")

CONFIG_FILE = Path("config.yml")
configuration = ConfigurationModel.read(CONFIG_FILE)
runs_api = RunsApi(configuration)
modules_api = ModulesApi(configuration)

DATABASE_FILE = "database.json"
DATABASE_LOCK_FILE = "database.lock"
JOB_NUMBER = 0
cdr_url = "https://api.cdr.land"

class Queue:
    def __init__(self, database_file: str):
        self._database_path = Path(DATABASE_FILE)

    def _read(self) -> list[str]:
        q = json.loads(self._database_path.read_text())
        return q

    def _write(self, q: list[str]) -> None:
        self._database_path.write_text(json.dumps(q))
        return 0

    def push_job(self, job: dict) -> None:
        lock = FileLock(DATABASE_LOCK_FILE)
        with lock:
            q = self._read()
            q.append(job)
            print(f"queue: {q}")
            self._write(q)
            return 0

    def pop_job(self) -> Optional[str]:
        lock = FileLock(DATABASE_LOCK_FILE)
        with lock:
            q = self._read()
            print(f"queue: {q}")
            if q:
                job = q.pop(0)
                self._write(q)
                return job
        return None
    
    def peek_job(self) -> Optional[str]: 
        lock = FileLock(DATABASE_LOCK_FILE)
        with lock:
            q = self._read()
            if q:
                return q[0]
        return None

    def get_length(self) -> Optional[int]:
        lock = FileLock(DATABASE_LOCK_FILE)
        with lock:
            q = self._read()
            return len(q)

    # only the producer should call this, at the start
    def reset(self) -> None:
        Path(DATABASE_LOCK_FILE).unlink(missing_ok=True)
        Path(DATABASE_FILE).unlink(missing_ok=True)
        self._write([])
        return 0

async def donwload_map(req):
    cog_id = req['cog_id']
    cog_url = req['cog_url']
    print(f"COG ID: {cog_id}")
    print(f"COG URL: {cog_url}")
    all_map_dir = os.getenv("TA1_INPUTS_DIR") + '/maps'
    if os.path.exists(os.path.join(all_map_dir, cog_id)):
        return {"ok": "success"}
    # Download .cog
    os.mkdir(os.path.join(all_map_dir, cog_id))
    map_dir = os.path.join(all_map_dir, cog_id)
    r = httpx.get(cog_url, timeout=1000)
    print(f"Downloading {cog_id} to {map_dir}")
    with open(os.path.join(map_dir, f"{cog_id}.tif"), "wb") as f:
        f.write(r.content)
    return {"ok": "success"}

def run_async_function(coroutine):
    return asyncio.run(coroutine)

def validate_request(data, signature_header, secret):
    """
    Validate the incoming request. This is a simple check to see if the
    request is JSON.
    """
    logging.debug("Validating request with signature %s", signature_header)
    hash_object = hmac.new(secret.encode("utf-8"), msg=data, digestmod=hashlib.sha256)
    expected_signature = hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        abort(403, "Request signatures didn't match")

def run_job(job_id: str, event_name: str) -> None:
    mip_body = {
        "job": job_id,
        "modules": [
                "georeference"
              ],
        "map": job_id,
        "force_rerun": False,
        "openai_key": "f4916dd7f1e424ec0154d5302d52a0143a147cfe35dd2730771582fb872d0477"
    }
    if event_name == 'feature_extract':
        all_job_status = True
        for module_name in ['line_extract', 'point_extract', 'polygon_extract']:
            mip_body["modules"] = [module_name]
            result = runs_api.post_run(mip_body)
            time.sleep(20)
            while True:
                try:
                    job_status = runs_api.get_run_by_name(result.run_id)              
                    if job_status.status.name == 'PASSED':
                        break      
                    elif job_status.status.name == 'FAILED':
                        break
                except FileNotFoundError:
                    time.sleep(10)
                time.sleep(10)
                print(job_id, module_name, job_status.status.name)
            job_status = runs_api.get_run_by_name(result.run_id)
            all_job_status = job_status and all_job_status
        return "PASSED" if all_job_status else "FAILED"

    elif event_name == 'georeference':
        result = runs_api.post_run(mip_body)
        time.sleep(20)
        while True:
            try:
                job_status = runs_api.get_run_by_name(result.run_id)                  
                if job_status.status.name == 'PASSED':
                    break      
                elif job_status.status.name == 'FAILED':
                    break
            except FileNotFoundError:
                time.sleep(100)
            time.sleep(10)      
        job_status = runs_api.get_run_by_name(result.run_id)   
        return job_status
    else:
        return "FAILED"
        
def gen_feature_payload(cog_id, feature_results):
    feature_payload = FeatureResults(
                            cog_id=cog_id,
                            polygon_feature_results=feature_results['polygon_extract'],
                            line_feature_results=feature_results['line_extract'],
                            point_feature_results=feature_results['point_extract'],
                            cog_area_extractions=[],
                            cog_metadata_extractions=[],
                            system=os.getenv("SYSTEM_NAME"),
                            system_version=os.getenv("SYSTEM_VERSION")
                        )
    return feature_payload

async def send_results_to_cdr(job_id: str, event: str):
    if event == 'feature_extract':
        feature_result_dict = {}
        for module in ['line_extract', 'point_extract', 'polygon_extract']:
            output_paths = modules_api.get_module_output_file_paths(job_id, module)
            mip_body = {
                "job": job_id,
                "modules": [
                        module
                      ],
                "map": job_id,
                "force_rerun": False,
                "openai_key": "f4916dd7f1e424ec0154d5302d52a0143a147cfe35dd2730771582fb872d0477"
            }
            feature2cdr_processor = feature4CDR(output_paths, mip_body)
            results = feature2cdr_processor.get_feature_list()
            feature_result_dict[module] = results 
    
        feature_payload = gen_feature_payload(job_id, feature_result_dict)
        headers = {'Authorization': f'Bearer {app.config["cdr_token"]}',\
              'accept': 'application/json',
              'Content-Type': 'application/json'}
        client = httpx.Client(follow_redirects=True)
        resp = client.post(f"{cdr_url}/v1/maps/publish/features",
                           data=feature_payload.model_dump_json(exclude_none=True), headers=headers, timeout=None)
    
        try:
            resp.raise_for_status()
            print(f"Posted Features to CDR! {job_id}")
        except Exception:          
            print(f"Failed to CDR! {job_id}")
        return resp.raise_for_status()
    
    elif event == 'georeference':
        output_paths = modules_api.get_module_output_file_paths(job_id, 'georeference')
        if output_paths == []:
            gcps = []
        else:
            georef2cdr_processor = georef4CDR(output_paths[0])
            gcps = georef2cdr_processor.get_all_gcps()
        
        results = GeoreferenceResults(**{
            "cog_id": job_id,
            "gcps": gcps,
            "georeference_results": [],
            "system": app.config["name"],
            "system_version": app.config["version"]
        })
        headers = {'Authorization': f'Bearer {app.config["cdr_token"]}',\
                  'accept': '*/*'}
        client = httpx.Client(follow_redirects=True)
        resp = client.post(f"{cdr_url}/v1/maps/publish/georef",
                           data={"georef_result": results.model_dump_json()}, files=[], headers=headers, timeout=None)
    
        try:
            resp.raise_for_status()
            print(f"Posted Georef to CDR! {job_id}")
        except Exception:          
            print(f"Failed to Georef CDR! {job_id}")
        return resp.raise_for_status()
    else:
        return f"Unknown event: {event}"

def log_cdr_paylod(payload):
    file_path = 'cdr_payload.json'
    # Open the JSON file in append mode
    with open(file_path, 'a+') as file:
        # Move cursor to the beginning of the file to read existing content
        file.seek(0)
        try:
            # Load existing JSON content if any
            json_data = json.load(file)
        except json.JSONDecodeError:
            # Handle the case where file is empty (no content)
            json_data = []

        # Append new data to the JSON data list
        json_data.append(data_to_append)

        # Move cursor to the beginning of the file to write new content
        file.seek(0)
        # Write JSON data back to the file
        json.dump(json_data, file, indent=4)
        # Ensure any remaining content is overwritten
        file.truncate()
    return

@app.post("/")
def producer_loop() -> None:
    queue = Queue(DATABASE_FILE)
     # check the signature
    validate_request(request.data, request.headers.get("x-cdr-signature-256"), current_app.config["callback_secret"])
    data = request.get_json()
    log_cdr_paylod(data)
    if  data["payload"].get('cog_id', None) is None or data["payload"].get('cog_url', None) is None:
        return {"ok": "success"}
    job, event = data["cog_id"], data["event"]
    run_async_function(donwload_map(data))
    if event == "map.process":
        print(f"Pushing job onto queue: {job}")
        queue.push_job({job: 'feature_extract'})
        queue.push_job({job: 'georeference'})
    return data

def consumer_loop(queue: Queue) -> None:
    while queue.get_length() != 0:
        job_dict = queue.peek_job()
        job_id, event_name = list(job_dict.keys())[0], list(job_dict.values())[0]
        job_status = run_job(job_id, event_name)
        print(f"Sending results to CDR: {job_id}")
        if job_status == 'PASSED':
            send_status = run_async_function(send_results_to_cdr(job_id, event_name))
        _ = queue.pop_job()
        sleep(2.0)


def main() -> int:
    if sys.argv[1] == "-p":
        app.run(host='0.0.0.0', port=8000)    
        producer_loop()
    elif sys.argv[1] == "-c":
        queue = Queue(DATABASE_FILE)
        consumer_loop(queue)
    else:
        raise Exception("not reached")
    return 1


if __name__ == '__main__':
    sys.exit(main())