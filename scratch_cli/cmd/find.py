from typing import Optional

import scratchattach as sa

from scratch_cli.context import context
from scratch_cli import rfmt
from scratch_cli import safmt

def find(*,
         offset: int,
         limit: int,
         user: Optional[str] = None,
         mode: Optional[str] = None,):

    if user:
        user: sa.User = context.session.connect_user(user)

        match mode:
            case "loved" | "loves":
                for project in user.loves(limit=limit, offset=offset):
                    rfmt.print_md(safmt.project(project))
            case "faved" | "faves" | "favorited" | "favorites":
                for project in user.favorites(limit=limit, offset=offset):
                    rfmt.print_md(safmt.project(project))
            case "shared" | None:
                for project in user.projects(limit=limit, offset=offset):
                    rfmt.print_md(safmt.project(project))
            case _:
                print(f"Invalid mode: {mode!r}")

        return

    print(f"{offset=}, {limit=}, {user=}, {mode=}")
