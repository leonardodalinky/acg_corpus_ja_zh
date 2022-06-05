import argparse
from glob import glob
from pathlib import Path

from tqdm import tqdm

from . import sentence_segmentation as ss


def register_subparser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        required=True,
        choices=["segment"],
        help="Type of preprocess to perform. `segment` means sentence segmentation.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        nargs="+",
        metavar="FILE",
        required=True,
        help="Path to input files. Glob pattern is supported.",
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
        "--cpu",
        action="store_true",
        default=False,
        help="Use CPU instead of GPU. Default: False.",
    )

    parser.set_defaults(func=main)


def main(args):
    # expand glob
    input_paths = []
    for input_path in args.input:
        input_paths.extend(glob(input_path))
    input_paths = [Path(path) for path in input_paths]
    for path in input_paths:
        assert path.exists(), f"Input file does not exist: {path}"
    output_path = Path(args.output)
    assert not output_path.exists() or output_path.is_dir(), f"Output path is not a directory: {output_path}"
    output_path.mkdir(parents=True, exist_ok=True)
    if args.type == "segment":
        pipeline = ss.get_default_pipeline(cpu_only=args.cpu)
        for path in tqdm(input_paths):
            output_file_path = output_path / f"{path.stem}_segmented.txt"
            sents = ss.split_sentences(pipeline, path.read_text("utf-8"))
            output_file_path.write_text("\n".join(sents), "utf-8")
