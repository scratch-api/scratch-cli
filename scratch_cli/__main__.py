import argparse

from scratch_cli.util import ERROR_MSG
from scratch_cli.__about__ import __version__

class _Args(argparse.Namespace):
    ...

def main():
    parser = argparse.ArgumentParser(
        prog='scratch',
        description='Scratch command line interface',
        epilog=f"Scratch CLI {__version__}"
    )

    args = parser.parse_args(namespace=_Args())

    try:
        cmd(args)
    except Exception as e:
        print(ERROR_MSG)
        raise e

def cmd(args: _Args) -> None:
    ...

if __name__ == '__main__':
    main()
