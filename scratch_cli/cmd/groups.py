from scratch_cli.cookies import cookies, t


def groups():
    for group in cookies.groups.values():
        print(f"{group.name!r}: {[sess.username for sess in group.sessions]}")
