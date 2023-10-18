def tree_csp_solver(csp):
    "[Fig. 6.11]"
    n = len(csp.vars)
    assignment = {}
    root = csp.vars[0]
    X, parent = topological_sort(csp.vars, root)
    for Xj in reversed(X):
        if not make_arc_consistent(parent[Xj], Xj, csp):
            return None
    for Xi in X:
        if not csp.curr_domains[Xi]:
            return None
        assignment[Xi] = csp.curr_domains[Xi][0]
    return assignment