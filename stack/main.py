#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

import argparse
import os
from pathlib import Path
import sys

from boto3.session import Session

from template_parameters import TemplateParameters
from stack import Stack

DEFAULT_OWNER_NAME = "mpg"
DEFAULT_KEY_NAME = "mpg-key"
DEFAULT_REGION = "us-west-2"
DEFAULT_REGION_AZ = "us-west-2a"
DEFAULT_INSTANCE_TYPE = "p2.8xlarge"
DEFAULT_DISK_GB = 250


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="deploy",
        description="Deploys a TA1 stack")

    # required config options
    parser.add_argument(
        "--stack-name",
        type=str,
        default=None,
    )

    # optional config options
    parser.add_argument(
        "--owner-name",
        type=str,
        default=DEFAULT_OWNER_NAME,
    )
    parser.add_argument(
        "--ec2_key_name",
        type=str,
        default=DEFAULT_KEY_NAME,
    )
    parser.add_argument(
        "--region",
        type=str,
        default=DEFAULT_REGION,
    )
    parser.add_argument(
        "--region-az",
        type=str,
        default=DEFAULT_REGION_AZ,
    )
    parser.add_argument(
        "--disk-gb",
        type=int,
        default=DEFAULT_DISK_GB,
    )
    parser.add_argument(
        "--instance-type",
        type=str,
        default=DEFAULT_INSTANCE_TYPE,
    )

    # actions
    parser.add_argument(
        "--create",
        action="store_true",
    )
    parser.add_argument(
        "--public-ip",
        action="store_true",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
    )

    args = parser.parse_args()
    do_create = args.create
    do_delete = args.delete
    do_public_ip = args.public_ip

    parameters = TemplateParameters(
        disk_gb=args.disk_gb,
        ec2_key_name=args.ec2_key_name,
        instance_type=args.instance_type,
        owner_name=args.owner_name,
        region=args.region,
        region_az=args.region_az,
        stack_name=args.stack_name,
    )

    if "_" in args.stack_name:
        parser.error("stack_name must not contain '_'")

    print("Stack:")
    print(parameters.to_yaml())

    client = Session().client("cloudformation")
    stack = Stack(client, parameters)

    if do_create:
        stack.create()
        stack.wait_on_creation()
        return 0

    if do_public_ip:
        ip = stack.get_public_ip()
        print(ip)
        return 0

    if do_delete:
        stack.delete()
        return 0

    print("error: no command given")
    return 1


if __name__ == "__main__":
    sys.exit(main())
