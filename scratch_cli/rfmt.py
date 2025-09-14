# formatting utilities. rfmt = reformat

from pathlib import Path

import re
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

def escape(text: str, *, disabled: bool = False) -> str:
    if disabled:
        return text

    # from python-telegram-bot
    special_chars_regex = r'([_*[\]()~`>#+\-=|{}.!])'
    ret = re.sub(special_chars_regex, r'\\\1', text)

    ret = ret.replace('\n', '  \n')  # force new lines, but not hard breaks

    return ret

if __name__ == '__main__':
    print_md(quote("Hey\nI\n\nAm a quote"))
    print_md(escape(quote("Hey\nI\n\nAm a quote")))
