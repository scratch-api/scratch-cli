import warnings

from getpass import getpass

import scratchattach as sa

from scratch_cli.typed_cookies import cookies
from scratch_cli import serialize

warnings.filterwarnings("ignore", category=sa.LoginDataWarning)


def login(login_by_sessid: bool):
    if login_by_sessid:
        sessid = getpass("SessID: ")

        sess = sa.login_by_id(sessid)
        if not sess.username:
            raise ValueError("Invalid session ID")
    else:
        username = input("Username: ")
        password = getpass()
        sess = sa.login(username, password)

    register_session(sess)


def register_session(sess: sa.Session):
    if cookies.current_group_name == '':
        group_name = sess.username.lower()
        cookies.groups |= {group_name: serialize.session(sess)}
        cookies.current_group_name = group_name
    else:
        ...
