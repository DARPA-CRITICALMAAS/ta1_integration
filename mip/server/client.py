#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

import argparse
import json
from pathlib import Path
import sys
from typing import Optional

import requests


class Options:
    def __init__(self):

        parser = argparse.ArgumentParser(
            prog="client",
            description="Simple client app for the mipper server")

        parser.add_argument(
            "--url", "-u",
            type=str,
            required=True,
            help=f"URL of the mipper server",
        )
        parser.add_argument(
            "--get", "-g",
            action="store_true",
            help="perform a GET request",
        )
        parser.add_argument(
            "--post", "-p",
            action="store_true",
            help="perform a POST request",
        )
        parser.add_argument(
            "--input", "-i",
            type=str,
            default=None,
            help="input json file (for POST requests)",
        )
        parser.add_argument(
            "--output", "-o",
            type=str,
            required=True,
            help="output json file",
        )

        args = parser.parse_args()

        self.url = args.url

        if not args.get and not args.post:
            parser.error("Either --get or --post must be specified")
        if args.get and args.post:
            parser.error("Only one of {--get, --post} must be specified")
        self.do_get = args.get
        self.do_post = args.post

        self.input: Optional[Path] = None
        if self.do_post:
            if not args.input:
                parser.error("--input is required with --post")
            self.input = Path(args.input)
        if self.do_get and args.input:
            parser.error("--input is not allowed with with --get")

        self.output = Path(args.output)


def main() -> int:

    options = Options()

    auth = None  # ('user', 'pass')

    if options.do_get:
        resp = requests.get(url=options.url, auth=auth)
        if resp.status_code != 200:
            print(f"*** error: {resp.content}")
        s = resp.json()
        print("-------------")
        print(s)
        print("-------------")
        options.output.write_text(json.dumps(s))

    if options.do_post:
        body = options.input.read_text()
        resp = requests.post(url=options.url, auth=auth, data=body)
        if resp.status_code != 200:
            print(f"*** error: {resp.content}")
        s = resp.json()
        print("-------------")
        print(s)
        print("-------------")
        options.output.write_text(json.dumps(s))

    return 0


if __name__ == '__main__':
    sts = main()
    sys.exit(sts)
