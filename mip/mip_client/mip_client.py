#!/usr/bin/env python3
# Copyright 2024 InferLink Corporation

import argparse
import json
from pathlib import Path
from pprint import pprint
import re
import sys
from typing import Optional

import requests


class Options:
    def __init__(self):

        parser = argparse.ArgumentParser(
            prog="client",
            description="Simple client app for the mipper mip_server")

        parser.add_argument(
            "--url", "-u",
            type=str,
            required=True,
            help=f"URL of the mipper mip_server",
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
            help="output file (typically json or zip)",
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

        self.output: Optional[Path] = None
        if args.output:
            self.output = Path(args.output)


def process_output(resp: requests.Response, output_file: Optional[Path]) -> int:
    content_type = resp.headers.get('content-type')
    if content_type == "application/json":
        s = resp.json()
        print("---------------------")
        pprint(s)
        print("---------------------")
        if output_file:
            output_file.write_text(json.dumps(s))
        return 0

    if content_type == "application/zip":
        size = resp.headers.get('content-length', None)
        if not output_file:
            cd = resp.headers.get("content-disposition")
            m = re.findall('filename=(.+)', cd)
            if m:
                f = m[0]
                if f[0] == '"' and f[-1] == '"':
                    f = f[1:-1]
                output_file = Path(f)
        if output_file:
            with open(output_file, 'wb') as fp:
                fp.write(resp.content)
            print("---------------------------------------")
            print(f"{output_file}: {size} bytes")
            print("---------------------------------------")
        else:
            # just print size, don't store the data
            print("---------------------------------------")
            print(f"{size} bytes (not stored)")
            print("---------------------------------------")
        return 0

    print(f"*** error: unsupported content type: {content_type}")
    return 1


def main() -> int:

    options = Options()

    auth = None  # ('user', 'pass')

    if options.do_get:
        resp = requests.get(url=options.url, auth=auth)
        if resp.status_code != 200:
            print(f"*** error: {resp.content}")
            return 1
        return process_output(resp, options.output)

    if options.do_post:
        body = options.input.read_text()
        resp = requests.post(url=options.url, auth=auth, data=body)
        if resp.status_code != 200:
            print(f"*** error: {resp.content}")
            return 1
        return process_output(resp, options.output)

    return 0


if __name__ == '__main__':
    sts = main()
    sys.exit(sts)
