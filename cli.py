import argparse
from data_clean.cli import register_subparser


parser = argparse.ArgumentParser(description="CLI for ACG dataset building.")
subparsers = parser.add_subparsers(help="Subcommand to run.")
# data_clean subcommand
register_subparser(subparsers.add_parser("clean", help="Clean the data."))


if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
