# stores 'global' variables used throughout the module
from dataclasses import dataclass
from typing import Optional

import scratchattach as sa

from scratch_cli.cookies import cookies

@dataclass
class _Context:
    _session: Optional[sa.Session] = None

    @property
    def session(self) -> sa.Session:
        if not self._session:
            self._session = next(cookies.sessions, None)

            if not self._session:
                raise RuntimeError("No session found. Try logging in?")

        return self._session

context = _Context()
