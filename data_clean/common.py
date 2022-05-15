from typing import *

__all__ = ["DocumentEpub", "filter_docs_by_threshold"]


class DocumentEpub:
    __REPR_TEXT_LEN__ = 20

    def __init__(self, text: str, title: Optional[str] = None, chapter_id: Optional[str] = None):
        assert text is not None
        self.text = text
        self.title = title
        self.chapter_id = chapter_id

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'<Document(title={self.title}, chapter_id={self.chapter_id}, len={len(self)}, text="{self.text[:self.__REPR_TEXT_LEN__]}")>'


def filter_docs_by_threshold(
    docs: List[DocumentEpub],
    threshold: float = 0.05,
    min_keep_len: int = 1000,
) -> List[DocumentEpub]:
    """
    Filter documents by the ratio of length. The percentage of documents that are filtered out is less than threshold.

    :param docs:
    :param threshold: the percentage of documents that are dropped.
    :param min_keep_len: if the length of a document is greater than this value, it will be kept.
    :return:
    """
    assert 0.0 <= threshold <= 1.0
    assert len(docs) > 0
    asc_docs = sorted(docs, key=lambda doc: len(doc))
    all_len = sum(len(doc) for doc in docs)
    filtered_docs = []
    for doc in asc_docs:
        if len(doc) > min_keep_len:
            break
        filtered_docs_len = sum(len(doc) for doc in filtered_docs)
        if (filtered_docs_len + len(doc)) / all_len < threshold:
            filtered_docs.append(doc)
    return [doc for doc in docs if doc not in filtered_docs]
