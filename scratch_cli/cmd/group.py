import argparse

from scratch_cli.typed_cookies import cookies


def print_all_groups():
    for _group in cookies.groups.values():
        print('-', _group["name"])

def none():
    if cookies.current_group_name == '':
        print(f"Listing all groups, not in a group")
        print_all_groups()
        return

    _group = cookies.current_group
    print(f"Reading members of {_group['name']!r}")

    for session in _group['sessions']:
        print('-', session['username'])

def switch():
    print(f"All groups::")
    print_all_groups()

    group_name = input("Enter group name: ")

    assert group_name in cookies.groups, f"invalid name {group_name!r}"

    cookies.current_group_name = group_name

def group(parser: argparse.ArgumentParser, cmd):
    match cmd:
        case None:
            none()
        case "switch":
            switch()
        case _:
            parser.print_help()
