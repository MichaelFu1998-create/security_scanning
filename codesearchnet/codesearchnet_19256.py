def closure(self, rules):
        """Fills out the entire closure based on some initial dotted rules.

        Args:
            rules - an iterable of DottedRules

        Returns: frozenset of DottedRules

        """
        closure = set()

        todo = set(rules)
        while todo:
            rule = todo.pop()
            closure.add(rule)

            # If the dot is at the end, there's no need to process it.
            if rule.at_end:
                continue

            symbol = rule.rhs[rule.pos]
            for production in self.nonterminals[symbol]:
                for first in self.first(rule.rest):
                    if EPSILON in production.rhs:
                        # Move immediately to the end if the production
                        # goes to epsilon
                        new_rule = DottedRule(production, 1, first)
                    else:
                        new_rule = DottedRule(production, 0, first)

                    if new_rule not in closure:
                        todo.add(new_rule)

        return frozenset(closure)