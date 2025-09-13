from scratch_cli.typed_cookies import cookies


def groups():
    for group in cookies.groups.values():
        print(f"{group}")
