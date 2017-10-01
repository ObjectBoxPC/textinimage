from argparse import ArgumentParser
import sys

def parse_args():
    arg_parser = ArgumentParser()
    subparsers = arg_parser.add_subparsers(title="operations",
        help="Operation",
        dest="operation")
    _add_embed_args(subparsers)
    _add_extract_args(subparsers)
    args = arg_parser.parse_args()
    if not args.operation:
        arg_parser.print_usage(file=sys.stderr)
        sys.exit(2)
    return args

def _add_embed_args(subparsers):
    parser = subparsers.add_parser("embed", help="Embed text in image")
    parser.add_argument("-i", "--input", help="Input image", required=True)
    text_group = parser.add_mutually_exclusive_group(required=True)
    text_group.add_argument("-t", "--text", help="Embed the given text")
    text_group.add_argument("--text-file", help="Embed the text from the file")
    parser.add_argument("-o", "--output", help="Output image", required=True)

def _add_extract_args(subparsers):
    parser = subparsers.add_parser("extract", help="Extract text from image")
    parser.add_argument("-i", "--input", help="Input image", required=True)
    parser.add_argument("-o", "--output",
        help="Output file (omit to write to standard output)")