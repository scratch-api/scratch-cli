import argparse
from typing import Literal, Optional

from scratch_cli import cmd
from scratch_cli.__about__ import __version__


class _Args(argparse.Namespace):
    command: Literal['login', 'group', 'groups', 'ungroup', None]

    # login
    login_by_sessid: bool

    # group
    group_command: Literal['switch', 'rename', 'delete', None]


def main():
    parser = argparse.ArgumentParser(
        prog='scratch',
        description='Scratch command line interface',
        epilog=f"Scratch CLI {__version__}"
    )

    # # # # # Commands # # # # #
    commands = parser.add_subparsers(dest="command")

    login = commands.add_parser("login", help="Login to Scratch")
    login.add_argument("--sessid", dest="login_by_sessid", action="store_true")

    group = commands.add_parser("group", help="Get current group info")
    group_commands = group.add_subparsers(dest="group_command")
    group_commands.add_parser("switch", help="Switch current group to another")
    group_commands.add_parser("delete", help="Delete the current group.")
    group_commands.add_parser("rename", help="Try to rename the group, if possible.")

    groups = commands.add_parser("groups", help="Get list of groups")
    ungroup = commands.add_parser("ungroup",
                                  help="This exits the current group and into the 'global' group. "
                                       "If you login now, it will make a new group with only 1 member, "
                                       "which you will automatically enter.")

    args = parser.parse_args(namespace=_Args())

    do_cmd(parser, args)


def do_cmd(parser: argparse.ArgumentParser, args: _Args) -> None:
    match args.command:
        case "login":
            cmd.login(args.login_by_sessid)
        case "group":
            cmd.group(parser, args.group_command)
        case "groups":
            cmd.groups()
        case "ungroup":
            cmd.ungroup()
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()
