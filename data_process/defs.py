from typing import *
from data_clean import DocumentEpub

__all__ = [
    "Document"
]


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
