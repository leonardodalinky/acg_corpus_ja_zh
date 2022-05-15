import json
import argparse
from pathlib import Path
from . import process


def register_subparser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        metavar="FILE",
        required=True,
        nargs="+",
        help="Path to source files.",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        metavar="FILE",
        required=True,
        nargs="+",
        help="Path to target files.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="DIR",
        required=True,
        help="Path to output file. Should be a directory.",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        metavar="INT",
        default=20,
        help="Number of overlaps to generate. Default: 20.",
    )
    parser.add_argument(
        "--max-align-size",
        type=int,
        metavar="INT",
        default=8,
        help="Maximum alignment size. Default: 8.",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        default=False,
        help="Use CPU instead of GPU. Default: False.",
    )

    parser.set_defaults(func=main)


def main(args):
    pairs = process.generate_text_pairs(args.source, args.target, args.overlap, args.max_align_size, args.cpu)
    output_dir = Path(args.output)
    assert not output_dir.exists() or output_dir.is_dir(), f"Output path is not a directory: {output_dir}"
    output_dir.mkdir(parents=True, exist_ok=True)
    for _src_path, _tgt_path, pair in zip(args.source, args.target, pairs):
        src_path = Path(_src_path)
        tgt_path = Path(_tgt_path)
        new_output_path = output_dir / (src_path.stem + "_" + tgt_path.stem + ".json")
        with new_output_path.open("w", encoding="utf-8") as f:
            json.dump(pair, f, indent=2, ensure_ascii=False)
