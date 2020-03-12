from library.argparse.cli import argparse_cli
from library.base.process import process_path


def main():
    uri, args = argparse_cli()
    process_path(uri, args, False)


if __name__ == "__main__":
    main()
