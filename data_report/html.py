import os
import json
from pathlib import Path
from typing import *


from string import Template

template = Template(
    """
<!DOCTYPE html>
<head><title>${filename}</title><meta charset="utf-8" /></head>
<body>
<script src="https://unpkg.com/alpinejs" defer></script>
<script>window.data = ${data};</script>
<div style="line-height: 1.5em" x-data="{ alignments: window.data }">
  <template x-for="l in alignments">
    <div style="display: flex; border-color: #ddd; border-style: solid; border-width: 0 0 1px">
      <div lang="ja" style="flex: 1 0 0">
        <template x-for="(p, i) in l.src_texts">
          <div style="display: flex">
            <span x-text="l.src_numbers[i]" style="flex: 0 0 5ch"></span>
            <span x-text="p"></span>
          </div>
        </template>
      </div>
      <div style="flex: 0 0 8px; border: #ddd; border-style: solid; border-width: 0 1px 0 0"></div>
      <div style="flex: 0 0 8px"></div>
      <div lang="zh" style="flex: 1 0 0">
        <template x-for="(p, i) in l.tgt_texts">
          <div style="display: flex">
            <span x-text="l.tgt_numbers[i]" style="flex: 0 0 5ch"></span>
            <span x-text="p"></span>
          </div>
        </template>
      </div>
    </div>
  </template>
</div>
</body>
""")


def make_html_report(input_file: Union[str, bytes, os.PathLike], output_file: Union[str, bytes, os.PathLike]) -> None:
    input_path = Path(input_file)
    output_path = Path(output_file)
    assert input_path.exists()
    filename = input_path.stem
    html_output = template.substitute(filename=filename, data=input_path.read_text("utf-8"))
    output_path.write_text(html_output, "utf-8")
