from scratch_cli.cookies import cookies


def sessions():
    for i, session in enumerate(cookies.sessions):
        print(f"{i}. {session.username}")
