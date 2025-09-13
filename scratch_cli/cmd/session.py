from scratch_cli.typed_cookies import cookies


def group():
    print(f"Reading members of {cookies.current_group_name!r}")

    for session in cookies.groups.get(cookies.current_group_name, {}).get("sessions", []):
        print(session)
