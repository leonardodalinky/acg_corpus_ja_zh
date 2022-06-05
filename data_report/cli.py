import argparse
from glob import glob
from pathlib import Path

from . import html


def register_subparser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "input",
        type=str,
        metavar="FILE",
        help="Make a html report of json output",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="FILE/DIR",
        help="Path to output file. Should be a directory or filepath.",
    )

    parser.set_defaults(func=main)


def main(args):
    if args.output is None:
        out_path = Path(args.input).with_suffix(".html")
    else:
        out_path = Path(args.output)
        if out_path.is_dir():
            out_path = out_path / Path(args.input).with_suffix(".html").stem
        else:
            out_path = Path(args.output)
    html.make_html_report(args.input, out_path)
