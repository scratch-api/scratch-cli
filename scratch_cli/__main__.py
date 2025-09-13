import argparse
from typing import Literal

from scratch_cli.util import ERROR_MSG
from scratch_cli.__about__ import __version__

class _Args(argparse.Namespace):
    command: Literal['login', None]

def main():
    parser = argparse.ArgumentParser(
        prog='scratch',
        description='Scratch command line interface',
        epilog=f"Scratch CLI {__version__}"
    )
    commands = parser.add_subparsers(dest="command")

    login = commands.add_parser("login", help="Login to Scratch")
    login.add_argument("username")
    login.add_argument("password")

    args = parser.parse_args(namespace=_Args())

    try:
        cmd(parser, args)
    except Exception as e:
        print(ERROR_MSG)
        raise e

def cmd(parser: argparse.ArgumentParser, args: _Args) -> None:
    match args.command:
        case "login":
            ...
        case _:
            parser.print_help()

if __name__ == '__main__':
    main()
