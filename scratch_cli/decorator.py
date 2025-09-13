from scratch_cli.typed_cookies import cookies
from scratch_cli.context import context

import scratchattach as sa

def sessionable(func):
    """
    Decorate a function that can be run once for every session. i.e. a follow is sessionable, but login is not.
    """
    def wrapper(*args, **kwargs):
        for sess in cookies.current_group["sessions"]:
            context.session = sa.login_by_id(sess["id"], username=sess["username"])
            func(*args, **kwargs)

    return wrapper
