import argparse

from scratch_cli.typed_cookies import cookies


def print_all_groups():
    for _group in cookies.groups.values():
        print('-', _group["name"])

def none():
    if cookies.current_group_id == '':
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

    cookies.current_group_id = group_name

def rename():
    assert cookies.current_group_id != '', "Not in a group"

    group_name = input(f"Enter new group name for {cookies.current_group['name']!r}: ")
    group_id = group_name.lower()

    assert group_id not in cookies.groups, f"Existing name {group_name!r}"
    assert group_id != '', "Invalid name"

    cookies.current_group |= {"name": group_name}

    _group = cookies.current_group
    new_groups = cookies.groups
    del new_groups[cookies.current_group_id]
    new_groups[group_id] = _group

    cookies.groups = new_groups
    cookies.current_group_id = group_id


def group(parser: argparse.ArgumentParser, cmd):
    match cmd:
        case None:
            none()
        case "switch":
            switch()
        case "rename":
            rename()
        case _:
            parser.print_help()
