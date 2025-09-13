# stores 'global' variables used throughout the module
from dataclasses import dataclass
from typing import Optional

import scratchattach as sa

from scratch_cli.typed_cookies import cookies

@dataclass
class _Context:
    _session: Optional[sa.Session] = None

    @property
    def group(self):
        return cookies.current_group

context = _Context()
