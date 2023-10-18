def SAT_plan(init, transition, goal, t_max, SAT_solver=dpll_satisfiable):
    "[Fig. 7.22]"
    for t in range(t_max):
        cnf = translate_to_SAT(init, transition, goal, t)
        model = SAT_solver(cnf)
        if model is not False:
            return extract_solution(model)
    return None