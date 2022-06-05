import unicodedata
from typing import *

import torch.cuda
from trankit import Pipeline

__all__ = ["get_default_pipeline", "split_sentences"]


def get_default_pipeline(cpu_only=False) -> Pipeline:
    return Pipeline("auto", gpu=not cpu_only and torch.cuda.is_available())


def split_sentences(pipeline: Pipeline, text: str) -> List[str]:
    """
    Split text into sentences.

    Example of `ssplit` result:
    {
        "text": "串焼きを凄く愛していると言いたいのだろうが、\n今の台詞を聞いて俺は吹き出してしまう。前も聞いたが、今やこいつの鉄板で笑えるネタだ。",
        "sentences": [
            {
                "id": 1,
                "text": "串焼きを凄く愛していると言いたいのだろうが、\n今の台詞を聞いて俺は吹き出してしまう。",
                "dspan": (0, 42)
            },
            {
                "id": 2,
                "text": "前も聞いたが、今やこいつの鉄板で笑えるネタだ。",
                "dspan": (42, 65)
            },
        ],
        "lang": "japanese"
    }

    :param pipeline: trankit pipeline
    :param text: text to be split
    :return:
    """
    results = pipeline.ssplit(text)
    texts = (sentence["text"] for sentence in results["sentences"])
    # replace some spaces with single space
    texts = (text.replace("\n", " ") for text in texts)
    texts = (text.replace("\t", " ") for text in texts)
    texts = (text.replace("\r", " ") for text in texts)
    # unicode normalization
    texts = (unicodedata.normalize("NFKC", text) for text in texts)
    texts = (text.strip() for text in texts)
    # must be non-empty
    texts = [text for text in texts if len(text) > 0]
    return texts
