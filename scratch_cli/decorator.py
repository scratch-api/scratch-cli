from scratch_cli.typed_cookies import cookies
from scratch_cli.context import context

import scratchattach as sa

class _ExitSessionLoop:
    pass

EXIT_SESSION_LOOP = _ExitSessionLoop()
"""
Return this to exit the session loop to save resources. Sessionable works by looping through sessions and calling your
function multiple times. If you return this, it will break.
"""

def sessionable(func):
    """
    Decorate a function that can be run once for every session. i.e. a follow is sessionable, but login is not.
    """
    def wrapper(*args, **kwargs):
        for sess in cookies.current_group["sessions"]:
            context.session = sa.login_by_id(sess["id"], username=sess["username"])
            if func(*args, **kwargs) is EXIT_SESSION_LOOP:
                break

    return wrapper
