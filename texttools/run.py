import argparse
import sys

from command import run_command, InvalidCommand

#TODO: update from __main__ version


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("-i", "--input")
    return parser.parse_args()


def run(args):
    input_text = args.input
    command = args.command
    try:
        result = run_command(input_text, command, multiline=False)
    except InvalidCommand as e:
        print(e)
        sys.exit(1)
    print(result)


if __name__ == "__main__":
    run(parse_arguments())
