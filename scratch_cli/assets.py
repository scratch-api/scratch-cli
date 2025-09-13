from pathlib import Path

import rich
from rich.markdown import Markdown

__file_path__ = Path(__file__).resolve()

path = __file_path__.parent / "assets"

def markdown_fmt(fp: str, /, **kwargs):
    return (path / fp).read_text().format(**kwargs)

def print_fmt(fp: str, /, **kwargs):
    return rich.print(Markdown(markdown_fmt(fp, **kwargs)))
