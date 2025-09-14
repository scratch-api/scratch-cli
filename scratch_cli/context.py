# stores 'global' variables used throughout the module
from dataclasses import dataclass
from typing import Optional

import scratchattach as sa

from scratch_cli.cookies import cookies, t

@dataclass
class _Context:
    _session: Optional[sa.Session] = None

    @property
    def session(self) -> sa.Session:
        if self._session is None:
            sess = cookies.current_group.sessions[0]
            self._session = sess.login

        return self._session

    @session.setter
    def session(self, session: sa.Session):
        self._session = session

context = _Context()
