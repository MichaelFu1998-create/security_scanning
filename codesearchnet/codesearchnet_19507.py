def sum_out(self, var, bn):
        "Make a factor eliminating var by summing over its values."
        vars = [X for X in self.vars if X != var]
        cpt = dict((event_values(e, vars),
                    sum(self.p(extend(e, var, val))
                        for val in bn.variable_values(var)))
                   for e in all_events(vars, bn, {}))
        return Factor(vars, cpt)