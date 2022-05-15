import io
import os
import sys
import json
import torch
import logging
import tempfile
from pathlib import Path
from typing import *
from sentence_transformers import SentenceTransformer
from contextlib import redirect_stdout


sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "vecalign")))
import vecalign.overlap as overlap
import vecalign.vecalign as valign


Alignment = Dict[str, List[int]]


__all__ = [
    "Alignment",
    "generate_alignments",
    "generate_multi_alignments",
    "generate_text_pairs",
]


def my_print_alignments(alignments, scores=None, file=sys.stdout):
    if scores is not None:
        for (x, y), s in zip(alignments, scores):
            print('%s:%s:%.6f' % (x, y, s))
    else:
        for x, y in alignments:
            print('%s:%s' % (x, y))


def generate_alignments(
    model: SentenceTransformer,
    src_file: Union[str, bytes, os.PathLike],
    tgt_file: Union[str, bytes, os.PathLike],
    n_overlaps=20,
    max_alignment_size=8,
) -> List[Alignment]:
    src_path = Path(src_file)
    tgt_path = Path(tgt_file)
    assert src_path.exists()
    assert tgt_path.exists()
    orig_argv = list(sys.argv)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        assert tmp_path.exists() and tmp_path.is_dir()
        src_overlap_path = tmp_path / f"{src_path.stem}.overlap"
        tgt_overlap_path = tmp_path / f"{tgt_path.stem}.overlap"
        # generate overlaps
        overlap.go(str(src_overlap_path), [str(src_path)], n_overlaps)
        overlap.go(str(tgt_overlap_path), [str(tgt_path)], n_overlaps)
        # generate embeddings
        src_embeddings = model.encode(src_overlap_path.read_text("utf-8").splitlines())
        tgt_embeddings = model.encode(tgt_overlap_path.read_text("utf-8").splitlines())
        src_embeddings_path = src_overlap_path.with_suffix(".overlap.embeddings")
        tgt_embeddings_path = tgt_overlap_path.with_suffix(".overlap.embeddings")
        # save embeddings
        src_embeddings.tofile(str(src_embeddings_path))
        tgt_embeddings.tofile(str(tgt_embeddings_path))
        logging.debug("Hook sys.argv")
        # align overlaps
        sys.argv = [
            orig_argv[0],
            "--src",
            str(src_path),
            "--tgt",
            str(tgt_path),
            "--src_embed",
            str(src_overlap_path),
            str(src_embeddings_path),
            "--tgt_embed",
            str(tgt_overlap_path),
            str(tgt_embeddings_path),
            "--alignment_max_size",
            str(max_alignment_size),
        ]
        logging.debug("Hook `print_alignments` method")
        valign.print_alignments = my_print_alignments
        with io.StringIO() as buf, redirect_stdout(buf):
            valign._main()
            align_output = buf.getvalue()
        logging.debug("Unhook `print_alignments` method")
        # parse alignments result
        lines = align_output.splitlines()
        lines = (line for line in lines if line.startswith("["))
        ret = []
        for line in lines:
            tmp = line.split(":")
            assert len(tmp) == 3
            ret.append(
                {
                    "src": json.loads(tmp[0]),
                    "tgt": json.loads(tmp[1]),
                }
            )
    sys.argv = orig_argv
    logging.debug("Unhook sys.argv")
    return ret


def generate_multi_alignments(
    src_filepaths: List[Union[str, bytes, os.PathLike]],
    tgt_filepaths: List[Union[str, bytes, os.PathLike]],
    n_overlaps=20,
    max_alignment_size=8,
    cpu_only=False,
) -> List[List[Alignment]]:
    assert len(src_filepaths) == len(tgt_filepaths), "src and tgt filepaths must have the same length"
    model = SentenceTransformer("sentence-transformers/LaBSE", device="cpu" if cpu_only or not torch.cuda.is_available() else "cuda")
    model.max_seq_length = 500
    ret = []
    for src_file, tgt_file in zip(src_filepaths, tgt_filepaths):
        ret.append(
            generate_alignments(model, src_file, tgt_file, n_overlaps=n_overlaps, max_alignment_size=max_alignment_size)
        )
    return ret


def generate_text_pairs(
    src_filepaths: List[Union[str, bytes, os.PathLike]],
    tgt_filepaths: List[Union[str, bytes, os.PathLike]],
    n_overlaps=20,
    max_alignment_size=8,
    cpu_only=False,
) -> List[List[Dict[str, Any]]]:
    assert len(src_filepaths) == len(tgt_filepaths), "src and tgt filepaths must have the same length"
    multi_aligns = generate_multi_alignments(src_filepaths, tgt_filepaths, n_overlaps=n_overlaps, max_alignment_size=max_alignment_size, cpu_only=cpu_only)
    ret = []
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
            tmp.append({
                "src_numbers": align["src"],
                "tgt_numbers": align["tgt"],
                "src_texts": src_line,
                "tgt_texts": tgt_line,
            })
        ret.append(tmp)
    return ret
