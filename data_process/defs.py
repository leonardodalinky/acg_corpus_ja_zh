import os
from typing import *
from pathlib import Path

from data_extract import DocumentEpub

__all__ = ["Document"]


class Document:
    def __init__(
        self,
        sentences: List[str],
        title: Optional[str] = None,
        chapter_id: Optional[str] = None,
    ):
        self.sentences = sentences
        self.title = title
        self.chapter_id = chapter_id

    def __str__(self):
        return "\n".join(self.sentences)

    def __repr__(self):
        return f"<{self.__class__.__name__}, title={self.title}, chapter_id={self.chapter_id}, sentences_count={len(self.sentences)}>"

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, item):
        return self.sentences[item]

    def __iter__(self):
        return iter(self.sentences)

    @classmethod
    def from_epub(cls, doc: DocumentEpub):
        sentences = []
        for sentence in doc.text.split("\n"):
            sentence = sentence.strip()
            if len(sentence) == 0:
                continue
            sentences.append(sentence)
        return cls(
            sentences=sentences,
            title=doc.title,
            chapter_id=doc.chapter_id,
        )

    def total_chars(self):
        """
        total number of characters in the document

        :return:
        """
        return sum([len(sentence) for sentence in self.sentences])

    def save(self, file_path: Union[str, bytes, os.PathLike]):
        def add_newline(ss: List[str]):
            for idx, s in enumerate(ss):
                if idx == len(ss) - 1:
                    yield s
                else:
                    yield s + "\n"

        with Path(file_path).open("w", encoding="utf-8") as f:
            f.writelines(add_newline(self.sentences))
