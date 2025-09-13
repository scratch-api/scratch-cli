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
                projects=safmt.collate(safmt.project, sess.loved_by_followed_users(limit=limit, offset=offset))
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
         mode: Optional[str] = None, ):
    if user:
        user: sa.User = context.session.connect_user(user)

        match mode:
            case "loved" | "loves":
                rfmt.print_fp(
                    "loves.md",
                    username=user.name,
                    projects=safmt.collate(safmt.project, user.loves(limit=limit, offset=offset))
                )

            case "faved" | "faves" | "favorited" | "favorites":
                rfmt.print_fp(
                    "faves.md",
                    username=user.name,
                    projects=safmt.collate(safmt.project, user.favorites(limit=limit, offset=offset))
                )

            case "shared" | None:
                rfmt.print_fp(
                    "shared.md",
                    username=user.name,
                    projects=safmt.collate(safmt.project, user.projects(limit=limit, offset=offset))
                )

            case _:
                print(f"Invalid mode: {mode!r}")

        return

    # assume we are in session mode
    find_in_session(
        offset=offset,
        limit=limit,
        mode=mode,
    )
