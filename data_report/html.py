import os
import json
from string import Template
from typing import *
from pathlib import Path

template = Template((Path(__file__).parent / "template.html").read_text("utf-8"))


def make_html_report(input_file: Union[str, bytes, os.PathLike], output_file: Union[str, bytes, os.PathLike]) -> None:
    input_path = Path(input_file)
    output_path = Path(output_file)
    assert input_path.exists()
    filename = input_path.stem
    html_output = template.substitute(filename=filename, data=input_path.read_text("utf-8"))
    output_path.write_text(html_output, "utf-8")
