def enumerate_joint(vars, e, P):
    """Return the sum of those entries in P consistent with e,
    provided vars is P's remaining variables (the ones not in e)."""
    if not vars:
        return P[e]
    Y, rest = vars[0], vars[1:]
    return sum([enumerate_joint(rest, extend(e, Y, y), P)
                for y in P.values(Y)])