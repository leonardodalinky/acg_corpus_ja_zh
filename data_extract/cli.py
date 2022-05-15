import argparse

from . import common
from . import epub
from data_process import Document
from pathlib import Path
from pathvalidate import sanitize_filename


def register_subparser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        required=True,
        choices=["epub"],
        help="Type of datasource to clean.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        metavar="FILE",
        required=True,
        help="Path to input file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="DIR",
        required=True,
        help="Path to output file. Should be a directory.",
    )

    group_epub = parser.add_argument_group("epub", "Additional arguments for epub manipulation.")
    group_epub.add_argument(
        "--threshold",
        type=float,
        metavar="FLOAT",
        default=0.05,
        help="The percentage of documents that are dropped. Default: 0.05.",
    )
    group_epub.add_argument(
        "--min-keep-len",
        type=int,
        metavar="INT",
        default=1000,
        help="If the length of a document is greater than this value, it will be kept. Default: 1000.",
    )

    parser.set_defaults(func=main)


def epub_extract(input_filepath: Path, output_dir: Path, threshold=0.05, min_keep_len=1000):
    epub_docs = epub.read_docs_from_epub(input_filepath)
    epub_docs = common.filter_docs_by_threshold(epub_docs, threshold, min_keep_len)
    docs = [Document.from_epub(doc) for doc in epub_docs]
    for idx, doc in enumerate(docs):
        filename = f"{idx}"
        filename += f"__{doc.chapter_id}" if doc.chapter_id else ""
        filename += f"__{doc.title}" if doc.title else ""
        filename += ".stage1"
        filename = sanitize_filename(filename)
        doc.save(output_dir / filename)


def main(args):
    input_path = Path(args.input)
    assert input_path.exists(), f"Input file does not exist: {input_path}"
    output_path = Path(args.output)
    assert not output_path.exists() or output_path.is_dir(), f"Output path is not a directory: {output_path}"
    output_path.mkdir(parents=True, exist_ok=True)
    if args.type == "epub":
        epub_extract(
            input_path,
            output_path,
            threshold=args.threshold,
            min_keep_len=args.min_keep_len,
        )
    else:
        raise NotImplementedError(f"{args.type} is not supported.")
