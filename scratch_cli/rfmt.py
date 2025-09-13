# formatting utilities. rfmt = reformat

from pathlib import Path

import rich
from rich.markdown import Markdown

__file_path__ = Path(__file__).resolve()

path = __file_path__.parent / "assets"

def md_fp(fp: str, /, **kwargs):
    return (path / fp).read_text().format(**kwargs)

def print_md(content: str, /):
    rich.print(Markdown(content))

def print_fp(fp: str, /, **kwargs):
    return print_md(md_fp(fp, **kwargs))

def quote(content: str, /):
    return '> ' + '\n> '.join(content.splitlines())

if __name__ == '__main__':
    print_md(quote("Hey\nI\n\nAm a quote"))
    