import argparse

from scratch_cli.__about__ import __version__

def main():
    parser = argparse.ArgumentParser(
        prog='scratch',
        description='Scratch command line interface',
        epilog=f"Scratch CLI {__version__}"
    )

    args = parser.parse_args()

if __name__ == '__main__':
    main()
