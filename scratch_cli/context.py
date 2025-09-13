# stores 'global' variables used throughout the module
from dataclasses import dataclass
from typing import Optional

import scratchattach as sa

@dataclass
class _Context:
    session: Optional[sa.Session] = None

context = _Context()
