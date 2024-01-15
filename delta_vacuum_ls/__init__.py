import argparse
import json
from urllib import parse
import sys

import deltalake
from more_itertools import chunked


def main():
    parser = argparse.ArgumentParser(
        prog="delta-vacuum-ls",
    )
    parser.add_argument("base_url")
    parser.add_argument("-0", "-z", dest='zero_terminated', help='zero terminated', action='store_true')
    parser.add_argument("-b", "--batch-size", type=int, default=100)
    parser.add_argument("-a", "--aws-s3api-delete", action='store_true')
    args = parser.parse_args()

    parsed = parse.urlparse(args.base_url)

    key_prefix = parsed.path.strip("/")

    dt = deltalake.DeltaTable(sys.argv[1], storage_options={'region': 'us-west-2'})
    files = list(dt.vacuum(0, enforce_retention_duration=False, dry_run=True))

    end = "\0" if args.zero_terminated else "\n"
    if args.aws_s3api_delete:
        for batch in chunked(files, args.batch_size):
            print(
                json.dumps(dict(Objects=[dict(Key=f"{key_prefix}/{key}") for key in batch])),
                end=end
            )
    else:
        for f in files:
            print(f, end=end)
