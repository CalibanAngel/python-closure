import argparse
import sys
from Grammar import Grammar
from Goto import GotoGenerator

parser = argparse.ArgumentParser(description="Simple TCP client")


def pars_arg():
    parser.add_argument("--fileInput", "-i",
                        help="the name of the file you want to read",
                        type=str,
                        default="rule.txt")
    parser.add_argument("--fileOutput", "-o",
                        help="the port of the file you want to create",
                        type=str,
                        default="output.txt")
    parser.add_argument("--verbose", "-v",
                        help="print all the process",
                        action="store_true")


def main():
    pars_arg()
    args = parser.parse_args()
    if args.fileInput == args.fileOutput:
        print("ERROR: you must give different name of files", file=sys.stderr)
        return 1
    raw_grammar = ""
    try:
        with open(args.fileInput, "r") as file:
            raw_grammar = file.read()
    except:
        print("ERROR: cannot open " + args.fileInput, file=sys.stderr)
        return 1
    g = Grammar(raw_grammar)
    g.parse()
    gotos = GotoGenerator(g)
    gotos.generate()
    gotos.display(args.verbose)
    gotos.create_file(args.fileOutput, args.verbose)

    return 0


if __name__ == "__main__":
    main()