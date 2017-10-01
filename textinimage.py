#!/usr/bin/env python3

from parse_args import parse_args
from embed_text import embed_text
from extract_text import extract_text

args = parse_args()

if args.operation == "embed":
    embed_text()
elif args.operation == "extract":
    extract_text()
else:
    print("Invalid operation???")
    sys.exit(1)