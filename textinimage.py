#!/usr/bin/env python3

from parse_args import parse_args
from embed_text import embed_text
from embed_text import embed_text_from_file
from extract_text import extract_text

args = parse_args()

if args.operation == "embed":
    if args.text:
        embed_text(args.input, args.output, args.text)
    elif args.text_file:
        embed_text_from_file(args.input, args.output, args.text_file)
    else:
        print("No text specified???")
        sys.exit(1)
elif args.operation == "extract":
    extract_text(args.input, args.output)
else:
    print("Invalid operation???")
    sys.exit(1)