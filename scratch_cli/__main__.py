import argparse
import warnings
from typing import Literal, Optional

from scratch_cli import cmd
from scratch_cli.__about__ import __version__


class _Args(argparse.Namespace):
    do_with_all: bool
    command: Literal['login', 'session', 'sessions', None]

    # login
    login_by_sessid: bool


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

    session = commands.add_parser("session", help="Get session info")
    sessions = commands.add_parser("sessions", help="Get list of sessions")

    args = parser.parse_args(namespace=_Args())

    do_cmd(parser, args)


def do_cmd(parser: argparse.ArgumentParser, args: _Args) -> None:
    if args.do_with_all:
        warnings.warn("Performing action with all accounts")

    match args.command:
        case "login":
            cmd.login(args.login_by_sessid)
        case "session":
            cmd.session()
        case "sessions":
            cmd.sessions()
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()
