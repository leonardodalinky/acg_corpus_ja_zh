import argparse
from glob import glob
from typing import List, Optional
from pathlib import Path

from . import tmx, html


def register_subparser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=["html", "tmx"],
        help="Type of visualization to perform. `html` means HTML report. `tmx` means TMX file.",
    )
    parser.add_argument(
        "input",
        type=str,
        nargs="*",
        metavar="FILE",
        help="Make a report from this file. Glob patterns are supported.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="FILE/DIR",
        help="Path to output file. Should be a directory or filepath. "
        "If not specified, the output file will be the same as the input file, but with corresponding extension.",
    )

    group_tmx = parser.add_argument_group("tmx", "Additional arguments for tmx transformations.")
    group_tmx.add_argument(
        "--src-lang",
        type=str,
        metavar="LANG",
        default="en",
        help="The language of the source language. Default: en.",
    )
    group_tmx.add_argument(
        "--tgt-lang",
        type=str,
        metavar="LANG",
        default=None,
        help="The language of the target language. Default: None.",
    )
    group_tmx.add_argument(
        "--list-langs",
        action="store_true",
        help="List all supported languages.",
    )

    parser.set_defaults(func=main)


def gen_input_path_and_output_path(in_paths: List[Path], out_path: Optional[Path], suffix=""):
    if len(in_paths) == 1:
        if out_path is None:
            yield in_paths[0], in_paths[0].with_suffix(suffix)
        else:
            if out_path.is_dir():
                yield in_paths[0], out_path / f"{in_paths[0].stem}.{suffix}"
            else:
                yield in_paths[0], out_path
    else:
        # multiple input files
        assert out_path is None or out_path.is_dir(), "If output is a filepath, only one input is allowed."
        if out_path is None:
            for in_path in in_paths:
                yield in_path, in_path.with_suffix(suffix)
        else:
            for in_path in in_paths:
                yield in_path, out_path / f"{in_path.stem}.{suffix}"


def main(args):
    if args.list_langs:
        print(tmx.list_langs())
        return

    # check type
    assert args.type is not None, "Type of visualization is not specified."
    # check input files
    assert args.input is not None and len(args.input) > 0, "Input files are not specified."

    in_paths = []
    for path in args.input:
        in_paths.extend(glob(path))
    in_paths: List[Path] = [Path(path) for path in in_paths]
    out_path = Path(args.output) if args.output else None
    if args.type == "html":
        for in_path, out_path in gen_input_path_and_output_path(in_paths, out_path, suffix=".html"):
            html.make_html_report(in_path, out_path)
    elif args.type == "tmx":
        for in_path, out_path in gen_input_path_and_output_path(in_paths, out_path, suffix=".tmx"):
            tmx.make_tmx_file(in_path, out_path, src_lang=args.src_lang, tgt_lang=args.tgt_lang)
