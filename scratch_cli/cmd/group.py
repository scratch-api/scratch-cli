import argparse
from typing import Optional

from scratch_cli.cookies import cookies, t
from scratch_cli.context import context
from scratch_cli.util import ERROR_MSG
from scratch_cli._args import Args as _Args

import scratchattach as sa

def print_all_groups():
    for _group in cookies.groups.values():
        print('-', _group.name)

def print_group_members():
    if cookies.current_group_id == '':
        print(f"Listing all groups, not in a group")
        print_all_groups()
        return

    _group = cookies.current_group
    print(f"Reading members of {_group.name!r}")

    for i, session in enumerate(_group.sessions):
        print(f"{i}. {session.username}")

def select_group_member(error: bool=True):
    """
    This will select a session and send it to context
    :return:
    """
    _group = cookies.current_group
    if len(_group.session_names) == 1:
        context.session = _group.sessions[0].login
        return
    elif len(_group.session_names) == 0:
        if error:
            raise Exception("No sessions")
        return

    print_group_members()
    selector = input("Select a group member: ")

    for sess in _group.sessions:
        if sess.username.lower() == selector.lower():
            context.session = sess.login
            return

    if selector.isnumeric():
        selector = int(selector)
        if selector < len(_group.session_names):
            context.session = _group.sessions[selector].login
            return

    if error:
        raise Exception(f"Invalid selection: {selector}")

def switch(group_name: Optional[str]):
    if not group_name:
        print(f"All groups:")
        print_all_groups()

        group_name = input("Enter group name: ")

    group_name = group_name.lower()
    assert group_name in cookies.groups, f"Invalid name {group_name!r}"

    cookies.current_group_id = group_name

def rename():
    assert cookies.current_group_id != '', "Not in a group"

    group_name = input(f"Enter new group name for {cookies.current_group.name!r}: ")
    group_id = group_name.lower()

    assert group_id not in cookies.groups or group_id == cookies.current_group_id, f"Existing name {group_name!r}"
    assert group_id != '', "Invalid name"

    cookies.current_group.name = group_name

    cookies.groups[group_id] = cookies.groups.pop(cookies.current_group_id)
    cookies.current_group_id = group_id


def group(parser: argparse.ArgumentParser, args: _Args):
    match args.group_command:
        case None:
            print_group_members()
        case "switch":
            switch(args.name)
        case "rename":
            rename()
        case "delete":
            raise NotImplementedError(ERROR_MSG)
        case _:
            parser.print_help()
