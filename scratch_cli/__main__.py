import argparse
from typing import Literal, Optional

from scratch_cli import cmd
from scratch_cli.__about__ import __version__


class _Args(argparse.Namespace):
    command: Literal['login', 'group', 'groups', 'ungroup', 'profile', 'find', 'config', None]

    # find
    offset: int
    limit: int
    user: Optional[str]
    mode: Optional[str]

    # login
    login_by_sessid: bool

    # group
    group_command: Literal['switch', 'rename', 'delete', None]

    # config
    config_command: Optional[str]


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

    profile = commands.add_parser("profile", help="View your profile")

    find = commands.add_parser("find",
                               help="Find projects, studios, etc.")
    find.add_argument("-O", "--offset", default=0, type=int, dest="offset",
                      help="Offset from which to start the search.")
    find.add_argument("-L", "--limit", default=10, type=int, dest="limit",
                      help="Offset from which to start the search.")
    find.add_argument("-U", "--user", dest="user",
                      help="User to search for projects (shared, loved, favorite)")
    find.add_argument("mode", nargs="?", help="What we are searching for")

    config = commands.add_parser("config", help="View your PUBLIC _SCLI_CONFIG_")
    config.add_subparsers(dest="config_command").add_parser("edit", help="Edit your scli config")

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
        case "profile":
            cmd.profile()
        case "find":
            cmd.find(
                offset=args.offset,
                limit=args.limit,
                user=args.user,
                mode=args.mode
            ),
        case "config":
            cmd.config(
                args.config_command
            )
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()
