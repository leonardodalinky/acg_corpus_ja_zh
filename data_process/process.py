import io
import os
import sys
import logging
from typing import *
from pathlib import Path
from contextlib import redirect_stdout

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "aligner")))
from bertalign import Encoder, Bertalign

Alignment = Dict[str, List[int]]


__all__ = [
    "Alignment",
    "generate_alignments",
    "generate_multi_alignments",
    "generate_text_pairs",
]


def generate_alignments(
    model: Encoder,
    src_file: Union[str, bytes, os.PathLike],
    tgt_file: Union[str, bytes, os.PathLike],
    max_alignment_size=8,
    top_k=5,
    win=5,
) -> List[Alignment]:
    src_path = Path(src_file)
    tgt_path = Path(tgt_file)
    assert src_path.exists()
    assert tgt_path.exists()

    # load text
    src_lines = src_path.read_text("utf-8").splitlines()
    src_lines = [line.strip() for line in src_lines]
    src_lines = [line for line in src_lines if line != ""]
    tgt_lines = tgt_path.read_text("utf-8").splitlines()
    tgt_lines = [line.strip() for line in tgt_lines]
    tgt_lines = [line for line in tgt_lines if line != ""]

    # align
    with io.StringIO() as buf, redirect_stdout(buf):
        aligner = Bertalign(
            model,
            "\n".join(src_lines),
            "\n".join(tgt_lines),
            max_align=max_alignment_size,
            top_k=top_k,
            win=win,
            is_split=True,
        )
        aligner.align_sents(cpu_only=(str(model.model.device) == "cpu"))
        results = aligner.result
    return [{"src": result[0], "tgt": result[1]} for result in results]


def generate_multi_alignments(
    src_filepaths: List[Union[str, bytes, os.PathLike]],
    tgt_filepaths: List[Union[str, bytes, os.PathLike]],
    max_alignment_size=8,
    top_k=5,
    win=5,
    cpu_only=False,
) -> List[List[Alignment]]:
    assert len(src_filepaths) == len(tgt_filepaths), "src and tgt filepaths must have the same length"
    model = Encoder(cpu_only=cpu_only)
    model.model.max_seq_length = 500
    ret = []
    logging.info("Generating alignments...")
    for src_file, tgt_file in zip(src_filepaths, tgt_filepaths):
        logging.info(f"Aligning {src_file} and {tgt_file}...")
        ret.append(
            generate_alignments(model, src_file, tgt_file, max_alignment_size=max_alignment_size, top_k=top_k, win=win)
        )
    return ret


def generate_text_pairs(
    src_filepaths: List[Union[str, bytes, os.PathLike]],
    tgt_filepaths: List[Union[str, bytes, os.PathLike]],
    max_alignment_size=8,
    top_k=5,
    win=5,
    cpu_only=False,
) -> List[List[Dict[str, Any]]]:
    assert len(src_filepaths) == len(tgt_filepaths), "src and tgt filepaths must have the same length"
    multi_aligns = generate_multi_alignments(
        src_filepaths, tgt_filepaths, max_alignment_size=max_alignment_size, top_k=top_k, win=win, cpu_only=cpu_only
    )
    ret = []
    logging.info("Generating text pairs...")
    for src_path, tgt_path, aligns in zip(src_filepaths, tgt_filepaths, multi_aligns):
        src_path = Path(src_path)
        tgt_path = Path(tgt_path)
        assert src_path.exists()
        assert tgt_path.exists()
        src_lines = src_path.read_text("utf-8").splitlines()
        tgt_lines = tgt_path.read_text("utf-8").splitlines()
        tmp = []
        for align in aligns:
            src_line = [src_lines[i] for i in align["src"]]
            tgt_line = [tgt_lines[i] for i in align["tgt"]]
            tmp.append(
                {
                    "src_numbers": align["src"],
                    "tgt_numbers": align["tgt"],
                    "src_texts": src_line,
                    "tgt_texts": tgt_line,
                }
            )
        ret.append(tmp)
    return ret
