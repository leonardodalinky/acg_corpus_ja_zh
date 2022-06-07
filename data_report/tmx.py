import os
import json
from typing import *
from pathlib import Path

from translate.lang import team
from translate.storage import tmx


def list_langs() -> List[str]:
    return list(team.LANG_TEAM_LANGUAGE_SNIPPETS.keys())


def json2tmx(json_obj: List[Dict[str, Any]], src_lang="en", tgt_lang: Optional[str] = None) -> tmx.tmxfile:
    ret = tmx.tmxfile()
    for block in json_obj:
        src_text = " ".join(block["src_texts"])
        tgt_text = " ".join(block["tgt_texts"])
        unit = tmx.tmxunit(src_text)
        unit.target = tgt_text
        unit.setsource(src_text, src_lang)
        unit.settarget(tgt_text, tgt_lang or "xx")
        ret.addunit(unit)
    return ret


def make_tmx_file(
    input_file: Union[str, bytes, os.PathLike],
    output_file: Union[str, bytes, os.PathLike],
    src_lang="en",
    tgt_lang: Optional[str] = None,
) -> None:
    input_path = Path(input_file)
    assert input_path.exists()
    with input_path.open("r", encoding="utf-8") as f:
        t = json2tmx(json.load(f), src_lang=src_lang, tgt_lang=tgt_lang)
        t.savefile(str(output_file))
