import argparse
from typing import Literal, Optional

from scratch_cli import cmd
from scratch_cli.__about__ import __version__


from scratch_cli._args import Args as _Args


def main():
    parser = argparse.ArgumentParser(
        prog='scratch',
        description='Scratch command line interface',
        epilog=f"Scratch CLI {__version__}"
    )

    if commands := parser.add_subparsers(dest="command"):
        if login := commands.add_parser("login", help="Login to Scratch"):
            login.add_argument("--sessid", dest="login_by_sessid", action="store_true")

        if group := commands.add_parser("group", help="Get current group info"):
            group_commands = group.add_subparsers(dest="group_command")
            if group_switch := group_commands.add_parser("switch", help="Switch current group to another"):
                group_switch.add_argument("name", nargs="?")

            group_commands.add_parser("delete", help="Delete the current group.")
            group_commands.add_parser("rename", help="Try to rename the group, if possible.")

        groups = commands.add_parser("groups", help="Get list of groups")
        ungroup = commands.add_parser("ungroup",
                                      help="This exits the current group and into the 'global' group. "
                                           "If you login now, it will make a new group with only 1 member, "
                                           "which you will automatically enter.")

        profile = commands.add_parser("profile", help="View your profile")

        if find := commands.add_parser("find",
                                       help="Find projects, studios, etc."):
            find.add_argument("-O", "--offset", default=0, type=int, dest="offset",
                              help="Offset from which to start the search.")
            find.add_argument("-L", "--limit", default=10, type=int, dest="limit",
                              help="Offset from which to start the search.")
            find.add_argument("-U", "--user", dest="username",
                              help="User to search for projects (shared, loved, favorite)")
            find.add_argument("-P", "--project", dest="project_id",
                              help="Project ID to search for")
            find.add_argument("mode", nargs="?", help="What we are searching for")

        if config := commands.add_parser("config", help="View your PUBLIC _SCLI_CONFIG_"):
            config.add_subparsers(dest="config_command").add_parser("edit", help="Edit your scli config")

    parser.add_argument("-U", "--user", dest="username",
                        help="Get user by name")

    parser.add_argument("-P", "--project", type=int, dest="project_id",
                        help="Get project by id")

    args = parser.parse_args(namespace=_Args())

    do_cmd(parser, args)


def do_cmd(parser: argparse.ArgumentParser, args: _Args) -> None:
    match args.command:
        case "login":
            cmd.login(args.login_by_sessid)
        case "group":
            cmd.group(parser, args)
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
                user=args.username,
                mode=args.mode,
                project=args.project_id
            ),
        case "config":
            cmd.config(
                args.config_command
            )
        case _:
            if args.username:
                cmd.find(user=args.username)
                return
            if args.project_id:
                cmd.find(project=args.project_id)
                return

            parser.print_help()


if __name__ == '__main__':
    main()
