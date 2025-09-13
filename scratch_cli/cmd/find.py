from typing import Optional

from scratch_cli.context import context
from scratch_cli import rfmt
from scratch_cli import safmt
import scratchattach as sa

def find(*,
         offset: int,
         limit: int,
         user: Optional[str] = None,
         mode: Optional[str] = None,):

    if user:
        user: sa.User = context.session.connect_user(user)

        match mode:
            case "shared" | _:
                for project in user.projects(limit=limit, offset=offset):
                    rfmt.print_md(safmt.project(project))

        return

    print(f"{offset=}, {limit=}, {user=}, {mode=}")
