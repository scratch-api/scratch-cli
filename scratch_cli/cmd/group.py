import argparse
from typing import Optional

from scratch_cli.typed_cookies import cookies
from scratch_cli.context import context
from scratch_cli import typed_cookies as t
from scratch_cli.util import ERROR_MSG

import scratchattach as sa

def print_all_groups():
    for _group in cookies.groups.values():
        print('-', _group["name"])

def print_group_members():
    if cookies.current_group_id == '':
        print(f"Listing all groups, not in a group")
        print_all_groups()
        return

    _group = cookies.current_group
    print(f"Reading members of {_group['name']!r}")

    for i, session in enumerate(_group['sessions']):
        print(f"{i}. {session['username']}")

def select_group_member(error: bool=True):
    """
    This will select a session and send it to context
    :return:
    """
    _group = cookies.current_group
    if len(_group['sessions']) == 1:
        sess = _group['sessions'][0]
        context.session = sa.login_by_id(sess["id"], username=sess["username"])
        return
    elif len(_group['sessions']) == 0:
        if error:
            raise Exception("No sessions")
        return

    print_group_members()
    selector = input("Select a group member: ")


    for sess in _group['sessions']:
        if sess['username'] == selector:
            context.session = sa.login_by_id(sess["id"], username=sess["username"])
            return

    if selector.isnumeric():
        selector = int(selector)
        if selector < len(_group['sessions']):
            sess = _group['sessions'][selector]
            context.session = sa.login_by_id(sess["id"], username=sess["username"])
            return

    if error:
        raise Exception(f"Invalid selection: {selector}")

def switch():
    print(f"All groups:")
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
            print_group_members()
        case "switch":
            switch()
        case "rename":
            rename()
        case "delete":
            raise NotImplementedError(ERROR_MSG)
        case _:
            parser.print_help()
