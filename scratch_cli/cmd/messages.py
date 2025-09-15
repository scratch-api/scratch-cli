from typing import Optional

from scratch_cli.context import context
from scratch_cli import rfmt, safmt
from scratch_cli.decorator import sessionable


@sessionable
def messages(offset: int,
             limit: Optional[int],
             filter_by: Optional[str],
             date: Optional[str]):
    sess = context.session
    if limit is None:
        limit = sess.message_count()

    rfmt.print_fp(
        "msgs.md",
        username=rfmt.escape(sess.username),
        activities=safmt.collate(safmt.activity,
                                 sess.messages(offset=offset, limit=limit, filter_by=filter_by, date_limit=date)),
    )
