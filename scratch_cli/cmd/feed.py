from typing import Optional

from scratch_cli.context import context
from scratch_cli.decorator import sessionable
from scratch_cli import rfmt, safmt

import scratchattach as sa

@sessionable
def whats_happening(offset, limit):
    sess = context.session
    user = sess.connect_linked_user()

    rfmt.print_fp(
        "feed.md",
        username=rfmt.escape(user.name),
        activities=safmt.collate(safmt.activity, sess.feed(offset=offset, limit=limit))
    )


def feed(mode: Optional[str] = None, offset: int = 0, limit: int = 10):
    sess = context.session
    user = sess.connect_linked_user()

    match mode:
        case None:
            whats_happening(offset, limit)
