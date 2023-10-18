def _compute_first(self):
        """Computes the FIRST set for every symbol in the grammar.

        Tenatively based on _compute_first in PLY.
        """
        for terminal in self.terminals:
            self._first[terminal].add(terminal)
        self._first[END_OF_INPUT].add(END_OF_INPUT)

        while True:
            changed = False

            for nonterminal, productions in self.nonterminals.items():
                for production in productions:
                    new_first = self.first(production.rhs)
                    if new_first - self._first[nonterminal]:
                        self._first[nonterminal] |= new_first
                        changed = True

            if not changed:
                break