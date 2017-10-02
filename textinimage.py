#!/usr/bin/env python3

from parse_args import parse_args
from embed_text import embed_text
from embed_text import embed_text_from_file
from extract_text import extract_text
import sys

args = parse_args()

def fail_with_error(message):
    print(message, file=sys.stderr)
    sys.exit(1)

try:
    if args.operation == "embed":
        if args.text:
            embed_text(args.input, args.output, args.text)
        elif args.text_file:
            embed_text_from_file(args.input, args.output, args.text_file)
        else:
            fail_with_error("PROGRAM BUG: No text specified")
    elif args.operation == "extract":
        extract_text(args.input, args.output)
    else:
        fail_with_error("PROGRAM BUG: Invalid operation")
except Exception as ex:
    fail_with_error("Error encountered: {} ({})".format(ex, type(ex).__name__))