import os
import re
import ebooklib
import unicodedata
from ebooklib import epub
from bs4 import BeautifulSoup
from pathlib import Path
from typing import *
from .common import DocumentEpub

__all__ = ["read_docs_from_epub"]


def read_docs_from_epub(file_path: Union[str, bytes, os.PathLike]) -> List[DocumentEpub]:
    """
    Read epub file and return a list of documents. Each document corresponds to a chapter.

    :param file_path: path to epub file
    :return:
    """
    ret = []
    for doc in _read_epub_to_text(file_path):
        ret.append(
            DocumentEpub(
                text=doc["text"],
                title=doc["title"],
                chapter_id=doc["file_stem"],
            )
        )
    return ret


def _read_epub_to_text(file_path: Union[str, bytes, os.PathLike]) -> List[Dict[str, Any]]:
    """
    Read epub file and return a list of text. Each text corresponds to a chapter.

    :param file_path: path to epub file
    :return:
        list of dict: {
            "title": str,
            "text": str or None,
            "file_stem": str or None,
        }
    """
    ebook = epub.read_epub(file_path)
    ret = []
    for uid, _ in ebook.spine:
        uid: str
        doc: epub.EpubItem = ebook.get_item_with_id(uid)
        if doc is None or doc.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        file_stem = Path(doc.get_name()).stem
        title = None
        for link in ebook.toc:
            if link.href.find(file_stem) != -1:
                title = _normalize_epub_text(link.title)
                break
        soup = BeautifulSoup(doc.get_content(), "lxml")
        ret.append(
            {
                "title": title if title is not None and len(title) > 0 else None,
                "file_stem": file_stem if file_stem is not None and len(file_stem) > 0 else None,
                "text": _normalize_epub_text(soup.get_text()),
            }
        )
    return ret


def _normalize_epub_text(text: Optional[str]) -> str:
    """
    Normalize epub text.

    :param text: epub text
    :return: normalized text
    """
    if text is None:
        return ""
    # replace multiple spaces with single space
    text = re.sub(r" +", " ", text)
    # replace \r
    text = re.sub(r"\r", "", text)
    # replace multiple new lines with single new line
    text = re.sub(r"\n+", "\n", text)
    # unicode normalization
    text = unicodedata.normalize("NFKC", text)
    return text.strip()
