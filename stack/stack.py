#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

from pathlib import Path
import time

from botocore.exceptions import ClientError
from mypy_boto3_cloudformation.client import CloudFormationClient

from template_parameters import TemplateParameters

DEFAULT_TEMPLATE_PATH = "./template.yml"
DEFAULT_WAIT_DELAY = 5
DEFAULT_WAIT_TIMEOUT = 120


# A Stack represents a "stack" (i.e. an AWS Cloud Formation template
# thing) and provides some operations on it, like create and delete.
class Stack:
    _CREATE_IN_PROGRESS = ["CREATE_IN_PROGRESS"]
    _CREATE_COMPLETED = ["CREATE_COMPLETE"]
    _DELETE_IN_PROGRESS = ["DELETE_IN_PROGRESS"]
    _DELETE_COMPLETED = ["DELETE_COMPLETE"]

    def __init__(
            self,
            client: CloudFormationClient,
            parameters: TemplateParameters) -> None:

        self._client = client
        self._parameters = parameters

    def create(self) -> None:
        params = [
            {
                "ParameterKey": "DiskGB",
                "ParameterValue": str(self._parameters.disk_gb),
            },
            {
                "ParameterKey": "EC2KeyName",
                "ParameterValue": self._parameters.ec2_key_name,
            },
            {
                "ParameterKey": "InstanceType",
                "ParameterValue": self._parameters.instance_type,
            },
            {
                "ParameterKey": "RegionAZ",
                "ParameterValue": self._parameters.region_az,
            },
            {
                "ParameterKey": "AMIId",
                "ParameterValue": self._parameters.ami_id,
            },
        ]

        tags: list[dict[str, str]] = [
            {
                "Key": "Owner",
                "Value": self._parameters.owner_name,
            },
        ]

        template = Path(DEFAULT_TEMPLATE_PATH).read_text()

        try:
            self._client.create_stack(
                StackName=self._parameters.stack_name,
                TemplateBody=template,
                Parameters=params,
                Tags=tags,
            )
        except ClientError as ex:
            raise ex

    def get_public_ip(self) -> str:
        data = self._client.describe_stacks(StackName=self._parameters.stack_name)
        outputs = data["Stacks"][0]["Outputs"]
        for output in outputs:
            if output["OutputKey"] == "PublicIp":
                return output["OutputValue"]
        raise KeyError("Public IP not found")

    def delete(self) -> None:
        self._client.delete_stack(StackName=self._parameters.stack_name)

    def wait_on_creation(self) -> None:
        self._wait_on_operation(
            waiting_strings=self._CREATE_IN_PROGRESS,
            completed_strings=self._CREATE_COMPLETED)

    def wait_on_deletion(self) -> None:
        self._wait_on_operation(
            waiting_strings=self._CREATE_IN_PROGRESS,
            completed_strings=self._CREATE_COMPLETED)

    # boto provides the "Waiter" class, but it doesn't allow for a
    # heartbeat (and also the handling of errors is unclear)
    def _wait_on_operation(
            self,
            waiting_strings: list[str],
            completed_strings: list[str],
            delay: int = DEFAULT_WAIT_DELAY, timeout: int = DEFAULT_WAIT_TIMEOUT) -> None:

        t = time.time()
        while True:
            d = self._client.describe_stacks(StackName=self._parameters.stack_name)
            status = d['Stacks'][0]['StackStatus']

            if status in waiting_strings:
                pass
            elif status in completed_strings:
                return
            else:
                raise Exception(f"waiter failed: {status}")

            elapsed = round(time.time() - t)
            if elapsed > timeout:
                raise Exception("waiter timed out")

            print(f"...{status}: {elapsed}s")
            time.sleep(delay)
