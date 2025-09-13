import argparse
import warnings
from typing import Literal, Optional

from scratch_cli import cmd
from scratch_cli.__about__ import __version__


class _Args(argparse.Namespace):
    do_with_all: bool
    command: Literal['login', 'group', 'groups', None]

    # login
    login_by_sessid: bool

    # group
    group_command: str


def main():
    parser = argparse.ArgumentParser(
        prog='scratch',
        description='Scratch command line interface',
        epilog=f"Scratch CLI {__version__}"
    )

    parser.add_argument("-A", "--all", action="store_true", help="Perform action with all accounts", dest="do_with_all")

    # # # # # Commands # # # # #
    commands = parser.add_subparsers(dest="command")

    login = commands.add_parser("login", help="Login to Scratch")
    login.add_argument("--sessid", dest="login_by_sessid", action="store_true")

    group = commands.add_parser("group", help="Get current group info")
    group_commands = group.add_subparsers(dest="group_command")
    group_commands.add_parser("switch", help="Switch current group to another")

    groups = commands.add_parser("groups", help="Get list of groups")
    ungroup = commands.add_parser("ungroup",
                                  help="This exits the current group and into the 'global' group. "
                                       "If you login now, it will make a new group with only 1 member, "
                                       "which you will automatically enter.")

    args = parser.parse_args(namespace=_Args())

    do_cmd(parser, args)


def do_cmd(parser: argparse.ArgumentParser, args: _Args) -> None:
    if args.do_with_all:
        warnings.warn("Performing action with all accounts")

    match args.command:
        case "login":
            cmd.login(args.login_by_sessid)
        case "group":
            cmd.group()
        case "groups":
            cmd.groups()
        case "ungroup":
            cmd.ungroup()
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()
