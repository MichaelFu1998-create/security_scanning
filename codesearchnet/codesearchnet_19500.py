def markov_blanket_sample(X, e, bn):
    """Return a sample from P(X | mb) where mb denotes that the
    variables in the Markov blanket of X take their values from event
    e (which must assign a value to each). The Markov blanket of X is
    X's parents, children, and children's parents."""
    Xnode = bn.variable_node(X)
    Q = ProbDist(X)
    for xi in bn.variable_values(X):
        ei = extend(e, X, xi)
        # [Equation 14.12:]
        Q[xi] = Xnode.p(xi, e) * product(Yj.p(ei[Yj.variable], ei)
                                         for Yj in Xnode.children)
    return probability(Q.normalize()[True])