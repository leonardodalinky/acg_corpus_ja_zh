import logging
import argparse
import data_clean.cli
import data_process.cli
import data_report.cli


logging.basicConfig(level=logging.INFO)


parser = argparse.ArgumentParser(description="CLI for ACG dataset building.")
subparsers = parser.add_subparsers(help="Subcommand to run.")
# data_clean subcommand
data_clean.cli.register_subparser(subparsers.add_parser("clean", help="Clean the data."))
# data_process subcommand
data_process.cli.register_subparser(subparsers.add_parser("process", help="Process the data."))
# data_report subcommand
data_report.cli.register_subparser(subparsers.add_parser("report", help="Report the data."))


if __name__ == "__main__":
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
