def goto(self, rules, symbol):
        """Computes the next closure for rules based on the symbol we got.

        Args:
            rules - an iterable of DottedRules
            symbol - a string denoting the symbol we've just seen

        Returns: frozenset of DottedRules
        """
        return self.closure(
            {rule.move_dot() for rule in rules
             if not rule.at_end and rule.rhs[rule.pos] == symbol},
        )