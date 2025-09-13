from scratch_cli.decorator import sessionable
from scratch_cli.context import context
from scratch_cli import rfmt

from scratch_cli import safmt

from rich.color import Color

RESET = "\x1b[0m"


@sessionable
def profile():
    user = context.session.connect_linked_user()
    rfmt.print_md(safmt.user_profile(user))
