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

    if cookies.current_group_id == '':
        group_name = sess.username.lower()

        i = 2
        old_name = group_name
        while group_name in cookies.groups:
            group_name = f"{old_name}_{i}"

        new_group: t.Group = t.Group(name= group_name, sessions=[serialized])

        cookies.groups |= {group_name: new_group}
        cookies.current_group_id = group_name
    else:
        cookies.current_group.sessions += [serialized]
