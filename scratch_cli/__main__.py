import argparse
from typing import Literal, Optional

from scratch_cli.login import login as cmd_login
from scratch_cli.context import context
from scratch_cli import cmd
from scratch_cli.util import ERROR_MSG
from scratch_cli.__about__ import __version__

class _Args(argparse.Namespace):
    command: Literal['login', None]

    # login
    login_by_sessid: bool

def main():
    parser = argparse.ArgumentParser(
        prog='scratch',
        description='Scratch command line interface',
        epilog=f"Scratch CLI {__version__}"
    )
    commands = parser.add_subparsers(dest="command")

    login = commands.add_parser("login", help="Login to Scratch")
    login.add_argument("--sessid", dest="login_by_sessid", action="store_true",)

    session = commands.add_parser("session", help="Get session info")

    args = parser.parse_args(namespace=_Args())

    try:
        do_cmd(parser, args)
    except Exception as e:
        raise Exception(ERROR_MSG) from e


def do_cmd(parser: argparse.ArgumentParser, args: _Args) -> None:
    match args.command:
        case "login":
            cmd_login(args.login_by_sessid)
        case "session":
            cmd.session()
        case _:
            parser.print_help()

if __name__ == '__main__':
    main()
