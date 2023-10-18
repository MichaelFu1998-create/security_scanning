def minimal_medium(model, min_objective_value=0.1, exports=False,
                   minimize_components=False, open_exchanges=False):
    """
    Find the minimal growth medium for the model.

    Finds the minimal growth medium for the model which allows for
    model as well as individual growth. Here, a minimal medium can either
    be the medium requiring the smallest total import flux or the medium
    requiring the least components (ergo ingredients), which will be much
    slower due to being a mixed integer problem (MIP).

    Arguments
    ---------
    model : cobra.model
        The model to modify.
    min_objective_value : positive float or array-like object
        The minimum growth rate (objective) that has to be achieved.
    exports : boolean
        Whether to include export fluxes in the returned medium. Defaults to
        False which will only return import fluxes.
    minimize_components : boolean or positive int
        Whether to minimize the number of components instead of the total
        import flux. Might be more intuitive if set to True but may also be
        slow to calculate for large communities. If set to a number `n` will
        return up to `n` alternative solutions all with the same number of
        components.
    open_exchanges : boolean or number
        Whether to ignore currently set bounds and make all exchange reactions
        in the model possible. If set to a number all exchange reactions will
        be opened with (-number, number) as bounds.

    Returns
    -------
    pandas.Series, pandas.DataFrame or None
        A series giving the import flux for each required import
        reaction and (optionally) the associated export fluxes. All exchange
        fluxes are oriented into the import reaction e.g. positive fluxes
        denote imports and negative fluxes exports. If `minimize_components`
        is a number larger 1 may return a DataFrame where each column is a
        minimal medium. Returns None if the minimization is infeasible
        (for instance if min_growth > maximum growth rate).

    Notes
    -----
    Due to numerical issues the `minimize_components` option will usually only
    minimize the number of "large" import fluxes. Specifically, the detection
    limit is given by ``integrality_tolerance * max_bound`` where ``max_bound``
    is the largest bound on an import reaction. Thus, if you are interested
    in small import fluxes as well you may have to adjust the integrality
    tolerance at first with
    `model.solver.configuration.tolerances.integrality = 1e-7` for instance.
    However, this will be *very* slow for large models especially with GLPK.

    """
    exchange_rxns = find_boundary_types(model, "exchange")
    if isinstance(open_exchanges, bool):
        open_bound = 1000
    else:
        open_bound = open_exchanges

    with model as mod:
        if open_exchanges:
            LOGGER.debug("Opening exchanges for %d imports.",
                         len(exchange_rxns))
            for rxn in exchange_rxns:
                rxn.bounds = (-open_bound, open_bound)
        LOGGER.debug("Applying objective value constraints.")
        obj_const = mod.problem.Constraint(
            mod.objective.expression, lb=min_objective_value,
            name="medium_obj_constraint")
        mod.add_cons_vars([obj_const])
        mod.solver.update()
        mod.objective = Zero
        LOGGER.debug("Adding new media objective.")
        tol = mod.solver.configuration.tolerances.feasibility

        if minimize_components:
            add_mip_obj(mod)
            if isinstance(minimize_components, bool):
                minimize_components = 1
            seen = set()
            best = num_components = mod.slim_optimize()
            if mod.solver.status != OPTIMAL:
                LOGGER.warning("Minimization of medium was infeasible.")
                return None
            exclusion = mod.problem.Constraint(Zero, ub=0)
            mod.add_cons_vars([exclusion])
            mod.solver.update()
            media = []
            for i in range(minimize_components):
                LOGGER.info("Finding alternative medium #%d.", (i + 1))
                vars = [mod.variables["ind_" + s] for s in seen]
                if len(seen) > 0:
                    exclusion.set_linear_coefficients(
                        dict.fromkeys(vars, 1))
                    exclusion.ub = best - 1
                num_components = mod.slim_optimize()
                if mod.solver.status != OPTIMAL or num_components > best:
                    break
                medium = _as_medium(exchange_rxns, tol, exports=exports)
                media.append(medium)
                seen.update(medium[medium > 0].index)
            if len(media) > 1:
                medium = pd.concat(media, axis=1, sort=True).fillna(0.0)
                medium.sort_index(axis=1, inplace=True)
            else:
                medium = media[0]
        else:
            add_linear_obj(mod)
            mod.slim_optimize()
            if mod.solver.status != OPTIMAL:
                LOGGER.warning("Minimization of medium was infeasible.")
                return None
            medium = _as_medium(exchange_rxns, tol, exports=exports)

    return medium