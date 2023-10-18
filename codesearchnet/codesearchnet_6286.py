def get_solution(model, reactions=None, metabolites=None, raise_error=False):
    """
    Generate a solution representation of the current solver state.

    Parameters
    ---------
    model : cobra.Model
        The model whose reactions to retrieve values for.
    reactions : list, optional
        An iterable of `cobra.Reaction` objects. Uses `model.reactions` by
        default.
    metabolites : list, optional
        An iterable of `cobra.Metabolite` objects. Uses `model.metabolites` by
        default.
    raise_error : bool
        If true, raise an OptimizationError if solver status is not optimal.

    Returns
    -------
    cobra.Solution

    Note
    ----
    This is only intended for the `optlang` solver interfaces and not the
    legacy solvers.
    """
    check_solver_status(model.solver.status, raise_error=raise_error)
    if reactions is None:
        reactions = model.reactions
    if metabolites is None:
        metabolites = model.metabolites

    rxn_index = list()
    fluxes = empty(len(reactions))
    reduced = empty(len(reactions))
    var_primals = model.solver.primal_values
    shadow = empty(len(metabolites))
    if model.solver.is_integer:
        reduced.fill(nan)
        shadow.fill(nan)
        for (i, rxn) in enumerate(reactions):
            rxn_index.append(rxn.id)
            fluxes[i] = var_primals[rxn.id] - var_primals[rxn.reverse_id]
        met_index = [met.id for met in metabolites]
    else:
        var_duals = model.solver.reduced_costs
        for (i, rxn) in enumerate(reactions):
            forward = rxn.id
            reverse = rxn.reverse_id
            rxn_index.append(forward)
            fluxes[i] = var_primals[forward] - var_primals[reverse]
            reduced[i] = var_duals[forward] - var_duals[reverse]
        met_index = list()
        constr_duals = model.solver.shadow_prices
        for (i, met) in enumerate(metabolites):
            met_index.append(met.id)
            shadow[i] = constr_duals[met.id]
    return Solution(model.solver.objective.value, model.solver.status,
                    Series(index=rxn_index, data=fluxes, name="fluxes"),
                    Series(index=rxn_index, data=reduced,
                           name="reduced_costs"),
                    Series(index=met_index, data=shadow, name="shadow_prices"))