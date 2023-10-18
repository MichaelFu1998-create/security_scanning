def fol_fc_ask(KB, alpha):
    """Inefficient forward chaining for first-order logic. [Fig. 9.3]
    KB is a FolKB and alpha must be an atomic sentence."""
    while True:
        new = {}
        for r in KB.clauses:
            ps, q = parse_definite_clause(standardize_variables(r))
            raise NotImplementedError