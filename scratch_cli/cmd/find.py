from typing import Optional

import scratchattach as sa

from scratch_cli.context import context
from scratch_cli import rfmt
from scratch_cli import safmt
from scratch_cli.decorator import sessionable

@sessionable
def find_in_session(*,
                    offset: int,
                    limit: int,
                    mode: Optional[str]):
    sess = context.session

    match mode.lower():
        case 'lovefeed':
            # Projects loved by scratchers I'm following

            rfmt.print_fp(
                "lovefeed.md",
                username=sess.username,
                projects='\n'.join(safmt.project(p) for p in sess.loved_by_followed_users(limit=limit, offset=offset))
            )
        case _:
            find(offset=offset,
                 limit=limit,
                 mode=mode,
                 user=sess.connect_linked_user())

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

    # assume we are in session mode
    find_in_session(
        offset=offset,
        limit=limit,
        mode=mode,
    )
