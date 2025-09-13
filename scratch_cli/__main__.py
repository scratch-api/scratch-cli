import argparse
from typing import Literal, Optional

from scratch_cli.login import login as cmd_login
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

    args = parser.parse_args(namespace=_Args())

    try:
        cmd(parser, args)
    except Exception as e:
        raise Exception(ERROR_MSG) from e

def cmd(parser: argparse.ArgumentParser, args: _Args) -> None:
    match args.command:
        case "login":
            cmd_login(args.login_by_sessid)
        case _:
            parser.print_help()

if __name__ == '__main__':
    main()
