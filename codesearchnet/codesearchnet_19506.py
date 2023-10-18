def pointwise_product(self, other, bn):
        "Multiply two factors, combining their variables."
        vars = list(set(self.vars) | set(other.vars))
        cpt = dict((event_values(e, vars), self.p(e) * other.p(e))
                   for e in all_events(vars, bn, {}))
        return Factor(vars, cpt)