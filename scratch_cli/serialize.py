# serialize scratchattach objects

import scratchattach as sa

from scratch_cli.cookies import cookies, t


def session(_session: sa.Session) -> t.Session:
    return t.Session(
        username=_session.username,
        id=_session.id
    )
