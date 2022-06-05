import json
import argparse
from pathlib import Path

import numpy as np

from . import process


def register_subparser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        metavar="FILE",
        required=True,
        nargs="+",
        help="Path to source files. Each source file is a text file, whose each line is in source language.",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        metavar="FILE",
        required=True,
        nargs="+",
        help="Path to target files. Each target file is a text file, whose each line is in target language.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="DIR",
        required=True,
        help="Path to output file. Should be a directory. The output files will be named as source file name + '_' + target file name + '.json'.",
    )
    parser.add_argument(
        "-m",
        "--max-align-size",
        dest="max_align_size",
        type=int,
        metavar="INT",
        default=8,
        help="Maximum alignment size. Default: 8.",
    )
    parser.add_argument(
        "-w",
        "--windows",
        type=int,
        metavar="INT",
        default=5,
        help="Window size for second pass. Default: 5.",
    )
    parser.add_argument(
        "-k",
        "--top-k",
        dest="top_k",
        type=int,
        metavar="INT",
        default=5,
        help="Top-k for second pass. Default: 5.",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        default=False,
        help="Use CPU instead of GPU. Default: False.",
    )

    parser.set_defaults(func=main)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def main(args):
    pairs = process.generate_text_pairs(
        args.source,
        args.target,
        max_alignment_size=args.max_align_size,
        top_k=args.top_k,
        win=args.windows,
        cpu_only=args.cpu,
    )
    output_dir = Path(args.output)
    assert not output_dir.exists() or output_dir.is_dir(), f"Output path is not a directory: {output_dir}"
    output_dir.mkdir(parents=True, exist_ok=True)
    for _src_path, _tgt_path, pair in zip(args.source, args.target, pairs):
        src_path = Path(_src_path)
        tgt_path = Path(_tgt_path)
        new_output_path = output_dir / (src_path.stem + "_" + tgt_path.stem + ".json")
        with new_output_path.open("w", encoding="utf-8") as f:
            json.dump(pair, f, indent=4, ensure_ascii=False, cls=NpEncoder)
