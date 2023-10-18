def add_lexicographic_constraints(model,
                                  objectives,
                                  objective_direction='max'):
    """
    Successively optimize separate targets in a specific order.

    For each objective, optimize the model and set the optimal value as a
    constraint. Proceed in the order of the objectives given. Due to the
    specific order this is called lexicographic FBA [1]_. This
    procedure is useful for returning unique solutions for a set of important
    fluxes. Typically this is applied to exchange fluxes.

    Parameters
    ----------
    model : cobra.Model
        The model to be optimized.
    objectives : list
        A list of reactions (or objectives) in the model for which unique
        fluxes are to be determined.
    objective_direction : str or list, optional
        The desired objective direction for each reaction (if a list) or the
        objective direction to use for all reactions (default maximize).

    Returns
    -------
    optimized_fluxes : pandas.Series
        A vector containing the optimized fluxes for each of the given
        reactions in `objectives`.

    References
    ----------
    .. [1] Gomez, Jose A., Kai Höffner, and Paul I. Barton.
    “DFBAlab: A Fast and Reliable MATLAB Code for Dynamic Flux Balance
    Analysis.” BMC Bioinformatics 15, no. 1 (December 18, 2014): 409.
    https://doi.org/10.1186/s12859-014-0409-8.

    """

    if type(objective_direction) is not list:
        objective_direction = [objective_direction] * len(objectives)

    constraints = []
    for rxn_id, obj_dir in zip(objectives, objective_direction):
        model.objective = model.reactions.get_by_id(rxn_id)
        model.objective_direction = obj_dir
        constraints.append(fix_objective_as_constraint(model))

    return pd.Series(constraints, index=objectives)