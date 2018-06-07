import argparse
import re
import sys

parser = argparse.ArgumentParser(description="Simple TCP client")


def pars_arg():
    parser.add_argument("--fileInput",
                        help="the name of the file you want to read",
                        type=str,
                        default="rule.txt")
    parser.add_argument("--fileOutput",
                        help="the port of the file you want to create",
                        type=str,
                        default="output.txt")


class Rule:
    def format(self):
        return "[R" + str(self.id) + "]: " + self.rule

    def print(self):
        print(self.format())

    def __init__(self, id):
        self.id = id
        self.rule = ""


class State:
    def format(self):
        tmp = "I" + self.id + "\n"
        for elem in self.states:
            tmp += "[" + elem + "] "
        return tmp

    def print(self):
        print(self.format())

    def __init__(self, id):
        self.id = id
        self.states = []


class Parser:
    rules = [Rule(0)]
    states = [State(0)]
    pattern_rule_name = re.compile("^R[1-9][\d]*$")
    pattern_rule = re.compile("^[A-Z]+>[A-Za-z+*()]+$")

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def parse_input_file(self):
        with open(self.input_file, "r") as file:
            for idx, line in enumerate(file, 1):
                if self.pattern_rule_name.match(line) and idx % 2 != 0:
                    self.rules.append(Rule(idx))
                elif self.pattern_rule.match(line) and idx % 2 == 0:
                    self.rules[int(idx / 2)].rule = line
                else:
                    print("ERROR: unexpected character in line " + str(idx), file=sys.stderr)
                    return 1
            self.rules[0].rule = "S>" + self.rules[1].rule.split(">")[0] + "\n"

    def compute(self):
        pass

    def create_output_file(self):
        with open(self.output_file, "w") as file:
            for elem in self.rules:
                file.write(elem.format())


def main():
    pars_arg()
    args = parser.parse_args()
    if args.fileInput == args.fileOutput:
        print("ERROR: you must give different name of files", file=sys.stderr)
        return 1
    file_parser = Parser(args.fileInput, args.fileOutput)
    file_parser.parse_input_file()
    file_parser.create_output_file()
    return 0


if __name__ == "__main__":
    main()