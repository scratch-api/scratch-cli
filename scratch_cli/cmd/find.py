from typing import Optional

from scratch_cli.context import context
from scratch_cli import rfmt
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
                    rfmt.print_fp(
                        "project.md",
                        title=project.title,
                        id=project.id,
                        author=project.author_name,
                    )

        return

    print(f"{offset=}, {limit=}, {user=}, {mode=}")
