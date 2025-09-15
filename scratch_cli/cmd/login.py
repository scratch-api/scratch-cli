import warnings

from getpass import getpass

import scratchattach as sa

from scratch_cli.cookies import cookies, t
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
    serialized = serialize.session(sess)
    session_name = sess.username.lower()

    cookies.sessions[session_name] = serialized

    if cookies.current_group_id == '':
        i = 2
        old_name = session_name
        while session_name in cookies.groups:
            session_name = f"{old_name}_{i}"

        new_group: t.Group = t.Group(name=session_name, session_names=t.CookieList([session_name]))

        cookies.groups[session_name] = new_group
        cookies.current_group_id = session_name
    else:
        cookies.current_group.sessions += [serialized]
