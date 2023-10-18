def all_events(vars, bn, e):
    "Yield every way of extending e with values for all vars."
    if not vars:
        yield e
    else:
        X, rest = vars[0], vars[1:]
        for e1 in all_events(rest, bn, e):
            for x in bn.variable_values(X):
                yield extend(e1, X, x)