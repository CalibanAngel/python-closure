import re
import sys
from Symbol import Symbol


class Production:
    def __init__(self, non_terminal, production, grammar, dot=0):
        self.non_terminal = non_terminal
        self.production = production
        self.grammar = grammar
        self.dot = dot

    def __eq__(self, other):
        return self.non_terminal == other.non_terminal and self.production == other.production and self.dot == other.dot

    def __str__(self):
        tmp = self.non_terminal + "->"
        found = False
        for idx, symbol in enumerate(self.production):
            if idx == self.dot:
                tmp += "."
                found = True
            tmp += "%s" % str(symbol.symbol)
        if not found:
            tmp += "."
        return tmp

    # Returns next symbol after dot.
    def next_symbol(self):
        if self.dot < len(self.production):
            return self.production[self.dot]
        return None

    # Increments the position of dot.
    def increment_dot(self):
        self.dot += 1

    # Returns True if next symbol is a terminal, otherwise False is returned.
    def is_next_terminal(self):
        return self.next_symbol().is_terminal()


class ProductionGenerator:
    pattern = re.compile("^[A-Z]>[A-Za-z+*\-()]*$")

    def __init__(self, raw_production, grammar):
        self.raw_production = raw_production
        self.grammar = grammar

    def generate(self):
        if not self.pattern.match(self.raw_production):
            print("ERROR: bad production rule", file=sys.stderr)
            sys.exit(1)
        left, right = self.raw_production.split(">")
        symbols = []
        for symbol in right:
            symbols.append(Symbol(symbol, self.grammar))
        return Production(left, symbols, self.grammar)

