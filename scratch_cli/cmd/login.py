import warnings

from getpass import getpass

import scratchattach as sa

from scratch_cli.cookies import cookies

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
    sessions = cookies.get("groups", {})

    cookies["groups"] = sessions
