class Symbol:
    def __init__(self, symbol, grammar):
        self.symbol = symbol
        self.grammar = grammar
        self.terminal = False

    def __str__(self):
        return self.symbol

    def __eq__(self, other):
        if isinstance(other, Symbol) and other.symbol == self.symbol:
            return True
        elif isinstance(other, int) and other == self.symbol:
            return True
        elif isinstance(other, str) and other == self.symbol:
            return True
        return False

    def is_terminal(self):
        if not self.terminal:
            self.terminal = self.symbol not in self.grammar.non_terminals
        return self.terminal

