def closures(self):
        """Computes all LR(1) closure sets for the grammar."""
        initial = self.initial_closure()
        closures = collections.OrderedDict()
        goto = collections.defaultdict(dict)

        todo = set([initial])
        while todo:
            closure = todo.pop()
            closures[closure] = closure

            symbols = {rule.rhs[rule.pos] for rule in closure
                       if not rule.at_end}
            for symbol in symbols:
                next_closure = self.goto(closure, symbol)

                if next_closure in closures or next_closure in todo:
                    next_closure = (closures.get(next_closure)
                                    or todo.get(next_closure))
                else:
                    closures[next_closure] = next_closure
                    todo.add(next_closure)

                goto[closure][symbol] = next_closure

        return initial, closures, goto