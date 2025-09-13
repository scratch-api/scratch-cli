from __future__ import annotations

from typing import Final, Optional


def ansi(code):
    return f"\u001b[{code}m"


GITHUB_REPO: Final[str] = "https://github.com/scratch-api/scratch-cli"
AURA: Final[str] = "-9999 aura 💀"
ERROR_MSG: Final[str] = f"{ansi(31)}{AURA}{ansi(0)}\nFile an issue on github: {GITHUB_REPO}/issues"

def split_trailing_number(self: str) -> tuple[str, str]:
    number = ""
    while len(self) and self[-1].isnumeric():
        number = self[-1] + number
        self = self[:-1]

    return self, number
