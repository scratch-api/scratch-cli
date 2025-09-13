import argparse

from scratch_cli.typed_cookies import cookies


def none():
    print(f"Reading members of {cookies.current_group_name!r}")

    for session in cookies.groups.get(cookies.current_group_name, {}).get("sessions", []):
        print(session)


def group(parser: argparse.ArgumentParser, cmd):
    match cmd:
        case None:
            none()
        case _:
            parser.print_help()
