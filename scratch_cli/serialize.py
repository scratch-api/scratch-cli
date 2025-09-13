# serialize scratchattach objects

import scratchattach as sa

import scratch_cli.typed_cookies as t


def session(_session: sa.Session) -> t.SESSION:
    return {
        "username": _session.username,
        "id": _session.id,
    }
