# stores 'global' variables used throughout the module
from dataclasses import dataclass
from typing import Optional

import scratchattach as sa

from scratch_cli.typed_cookies import cookies

@dataclass
class _Context:
    _session: Optional[sa.Session] = None

    @property
    def session(self) -> sa.Session:
        if self._session is None:
            sess = cookies.current_group["sessions"][0]
            self._session = sa.login_by_id(sess["id"], username=sess["username"])

        return self._session

    @session.setter
    def session(self, session: sa.Session):
        self._session = session

context = _Context()
