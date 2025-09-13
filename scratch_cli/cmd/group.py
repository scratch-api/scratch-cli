import argparse

from scratch_cli.typed_cookies import cookies


def none():
    if cookies.current_group_name == '':
        print(f"Listing all groups, not in a group")
        for _group in cookies.groups.values():
            print('-', _group["name"])
        return

    _group = cookies.current_group
    print(f"Reading members of {_group['name']!r}")

    for session in _group['sessions']:
        print('-', session['username'])


def group(parser: argparse.ArgumentParser, cmd):
    match cmd:
        case None:
            none()
        case _:
            parser.print_help()
