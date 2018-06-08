import copy
from Production import ProductionGenerator, Production


class Grammar:
    def __init__(self, raw_grammar):
        self.raw_grammar = raw_grammar
        self.grammar = []
        self.non_terminals = []
        self.terminals = []

    def __str__(self):
        tmp = ""
        for production in self.grammar:
            tmp += str(production) + "\n"
        return tmp

    def parse(self):
        for idx, line in enumerate(self.raw_grammar.split("\n")):
            if idx % 2 == 0:
                continue
            production = ProductionGenerator(line, self).generate()
            self.grammar.append(production)

        if len(self.grammar) > 1:
            self.grammar.insert(0, ProductionGenerator(("S>" + self.grammar[0].non_terminal), self).generate())

        for production in self.grammar:
            for symbol in production.production:
                if symbol.symbol not in self.terminals:
                    self.terminals.append(symbol.symbol)
            if production.non_terminal not in self.non_terminals:
                self.non_terminals.append(production.non_terminal)

        for symbol in self.non_terminals:
            if symbol in self.terminals: self.terminals.remove(symbol)

    def get_dot_terminal_productions(self):
        tmp = []
        for production in self.grammar:
            dot_indexes = [i for i, symbol in enumerate(production.production) if symbol.symbol in self.terminals]
            for idx in dot_indexes:
                new_production = copy.copy(production)
                new_production.dot = idx
                tmp.append(new_production)

        print("\nList of Productions that has dot before terminals:")

        for production in tmp:
            print(str(production))
        return tmp

    def get_alpha_dot_productions(self):
        tmp = []
        for production in self.grammar:
            new_production = copy.copy(production)
            new_production.dot = len(new_production.production)
            tmp.append(new_production)

        print("\nList of Productions that has dot at the end:")
        for production in tmp:
            print(str(production))
        return tmp
