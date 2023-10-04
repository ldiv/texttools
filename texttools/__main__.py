import argparse
import sys

from .command import run_command, chainables, scalars


class AvailableOperationsHelpFormatter(argparse.HelpFormatter):
    def _format_usage(self, usage, actions, groups, prefix):
        command_signature = "operation[->operation...]"
        example_command = """$ echo "  hello world! " | python -m texttools "trim->remove('!')->title_case" """
        example_result = "$ Hello world"
        example = f"Example:\n{example_command}\n{example_result}"
        operations = f"Operations\n{get_operations()}"
        usage = super()._format_usage(usage, actions, groups, prefix)
        return f"{usage}\n\n{example}\n\n{operations}\n\n"


def get_operations() -> str:
    chainable_ops = "Chainables:\n" + "\n".join([name for name in chainables.keys()])
    scalar_ops = "Scalars:\n" + "\n".join([name for name in scalars.keys()])
    return f"{chainable_ops}\n\n{scalar_ops}"


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="python -m texttools",
        description="A command line interface for texttools",
        formatter_class=AvailableOperationsHelpFormatter
    )
    parser.add_argument(
        "infile",
        nargs="?",  # This argument is optional
        type=argparse.FileType(encoding="utf-8"),
        help="File source for the text to transform, default is stdin",
        default=sys.stdin
    )
    parser.add_argument(
        "outfile",
        nargs="?",  # This argument is optional
        type=argparse.FileType("w", encoding="utf-8"),
        help="File destination for result, default is stdout",
        default=sys.stdout
    )
    parser.add_argument(
        "-m",
        "--multiline",
        help="Apply multiline mode to command",
        action="store_true"
    )
    parser.add_argument(
        "-w",
        "--word",
        help="Apply word mode to all transforms where it is applicable",
        action="store_true"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Display information about running command",
        action="store_true"
    )
    parser.add_argument(
        "command",
        help="The command to perform on the text",
        # TODO: add function for type
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    infile = args.infile
    outfile = args.outfile

    with infile, outfile:
        try:
            text = infile.read()
            if args.verbose:
                print(f"Running: '{args.command}' multiline: {args.multiline}")
            result = run_command(text, args.command, multiline=args.multiline)
            outfile.write(result)
            outfile.write('\n')
        except Exception as e:
            raise SystemExit(e)


if __name__ == "__main__":
    main()
