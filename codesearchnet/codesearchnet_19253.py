def _compute_follow(self):
        """Computes the FOLLOW set for every non-terminal in the grammar.

        Tenatively based on _compute_follow in PLY.
        """
        self._follow[self.start_symbol].add(END_OF_INPUT)

        while True:
            changed = False

            for nonterminal, productions in self.nonterminals.items():
                for production in productions:
                    for i, symbol in enumerate(production.rhs):
                        if symbol not in self.nonterminals:
                            continue

                        first = self.first(production.rhs[i + 1:])
                        new_follow = first - set([EPSILON])
                        if EPSILON in first or i == (len(production.rhs) - 1):
                            new_follow |= self._follow[nonterminal]

                        if new_follow - self._follow[symbol]:
                            self._follow[symbol] |= new_follow
                            changed = True

            if not changed:
                break