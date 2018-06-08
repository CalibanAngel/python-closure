import copy
import sys

MAX_LOOP = 30


class Goto:
    def __init__(self, productions, closure, parent_goto, id):
        self.productions = productions
        self.closure = closure
        self.parent_goto = parent_goto
        self.id = id

    def __str__(self):
        return "GOTO(%s, %s) => %d" % (self.parent_goto, self.closure, self.id)

    def __eq__(self, other):
        if len(self.productions) != len(other.productions):
            return False
        for production in other.productions:
            if not self.has_production(production):
                return False
        return True

    def has_production(self, other_production):
        for production in self.productions:
            if production == other_production:
                return True
        return False


class GotoGenerator:
    def __init__(self, grammar):
        self.grammar = grammar
        self.gotos = []
        ret = [self.grammar.grammar[0]]
        self.rec_non_terminal_lookup(ret[0], ret)
        self.first_closure = Goto(ret, "", None, 0)
        self.goto_dict = {}
        self.expected_id = 0

    # Generate Gotos and its productions from the given grammar.
    def generate(self):
        productions = self.first_closure.productions
        gotos_index = 0
        parent_goto = 0
        prev_parent_goto = 0

        while True:
            symbols_after_dot = self.get_symbols_after_dot(productions)

            for symbol in symbols_after_dot:
                # NOTE: Goto sequence number should never decrease.
                if parent_goto >= prev_parent_goto:
                    # Generate goto sequence from productions.
                    new_goto = self.get_goto(productions, symbol, parent_goto)
                    self.gotos.append(new_goto)

            if gotos_index >= len(self.gotos):
                # When there are no more gotos, end the loop.
                break

            # Next set of productions are from the calculated gotos.
            productions = self.gotos[gotos_index].productions

            if parent_goto >= prev_parent_goto:
                prev_parent_goto = parent_goto

            parent_goto = self.gotos[gotos_index].id
            gotos_index += 1

            if gotos_index > MAX_LOOP:
                print("ERROR: MAX LOOP EXCEEDED.")
                break

        self.fill_goto_dict()

    # Returns a list of symbols after dot from productions in a sequential way. Duplicate symbols are not added.
    def get_symbols_after_dot(self, productions):
        symbols_after_dot = []
        for production in productions:
            next_symbol = production.next_symbol()
            if next_symbol and next_symbol not in symbols_after_dot:
                symbols_after_dot.append(next_symbol)

        return symbols_after_dot

    # If the production has non terminal after dot, list all the productions of the terminal recursively and appends it to ret
    def rec_non_terminal_lookup(self, given_production, ret):
        rec_productions = []
        if given_production and given_production.next_symbol() and not given_production.is_next_terminal():
            for production in self.grammar.grammar:
                if production.non_terminal == given_production.next_symbol().symbol and production not in ret:
                    rec_productions.append(production)
                    if production not in ret:
                        ret.append(production)

        for production in rec_productions:
            self.rec_non_terminal_lookup(production, ret)

    def fill_goto_dict(self):
        for goto in self.gotos:
            self.goto_dict[str(goto.parent_goto) + str(goto.closure)] = goto

    # Generates goto sequence from given productions.
    def get_goto(self, productions, symbol, parent_goto):
        # E.g. if we have to calculate GOTO[1, s], then
        # 	symbol = s
        # 	parent_goto = 1

        ret = []
        for production in productions:
            if production.next_symbol() == symbol:
                new_production = copy.copy(production)
                new_production.increment_dot()
                ret.append(new_production)

        # Check for non-terminal after dot.
        for production in ret:
            self.rec_non_terminal_lookup(production, ret)

        # Check for duplicate goto. If so, decrement expected id.
        self.expected_id += 1
        r_goto = Goto(ret, symbol, parent_goto, self.expected_id)
        for goto in self.gotos:
            if r_goto == goto:
                r_goto.id = goto.id
                self.expected_id -= 1
                break
        return r_goto

    # Displays the generated Goto sequences.
    def display(self, verbose):
        if not verbose:
            return
        print("Closure => 0")
        for production in self.first_closure.productions:
            print(str(production))

        for goto in self.gotos:
            print(str(goto))
            for production in goto.productions:
                print(str(production))
            print("")

    def create_file(self, file_name, verbose):
        tmp = self.gotos
        if not verbose:
            tmp = self.verbose()
        try:
            with open(file_name, "w") as file:
                file.write("I" + str(self.first_closure.id) + "\n")
                for production in self.first_closure.productions:
                    file.write("[" + str(production) + "]")
                file.write("\n")
                for goto in tmp:
                    file.write("I"+ str(goto.id) + "\n")
                    for production in goto.productions:
                        file.write("[" + str(production) + "]")
                    file.write("\n")
        except:
            print("ERROR: cannot open " + file_name, file=sys.stderr)
            return 1

    def verbose(self):
        tmp = []
        for goto in self.gotos:
            if goto not in tmp:
                tmp.append(goto)
        return tmp
