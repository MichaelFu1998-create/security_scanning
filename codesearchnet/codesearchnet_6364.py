def production_envelope(model, reactions, objective=None, carbon_sources=None,
                        points=20, threshold=None):
    """Calculate the objective value conditioned on all combinations of
    fluxes for a set of chosen reactions

    The production envelope can be used to analyze a model's ability to
    produce a given compound conditional on the fluxes for another set of
    reactions, such as the uptake rates. The model is alternately optimized
    with respect to minimizing and maximizing the objective and the
    obtained fluxes are recorded. Ranges to compute production is set to the
    effective
    bounds, i.e., the minimum / maximum fluxes that can be obtained given
    current reaction bounds.

    Parameters
    ----------
    model : cobra.Model
        The model to compute the production envelope for.
    reactions : list or string
        A list of reactions, reaction identifiers or a single reaction.
    objective : string, dict, model.solver.interface.Objective, optional
        The objective (reaction) to use for the production envelope. Use the
        model's current objective if left missing.
    carbon_sources : list or string, optional
       One or more reactions or reaction identifiers that are the source of
       carbon for computing carbon (mol carbon in output over mol carbon in
       input) and mass yield (gram product over gram output). Only objectives
       with a carbon containing input and output metabolite is supported.
       Will identify active carbon sources in the medium if none are specified.
    points : int, optional
       The number of points to calculate production for.
    threshold : float, optional
        A cut-off under which flux values will be considered to be zero
        (default model.tolerance).

    Returns
    -------
    pandas.DataFrame
        A data frame with one row per evaluated point and

        - reaction id : one column per input reaction indicating the flux at
          each given point,
        - carbon_source: identifiers of carbon exchange reactions

        A column for the maximum and minimum each for the following types:

        - flux: the objective flux
        - carbon_yield: if carbon source is defined and the product is a
          single metabolite (mol carbon product per mol carbon feeding source)
        - mass_yield: if carbon source is defined and the product is a
          single metabolite (gram product per 1 g of feeding source)

    Examples
    --------
    >>> import cobra.test
    >>> from cobra.flux_analysis import production_envelope
    >>> model = cobra.test.create_test_model("textbook")
    >>> production_envelope(model, ["EX_glc__D_e", "EX_o2_e"])

    """

    reactions = model.reactions.get_by_any(reactions)
    objective = model.solver.objective if objective is None else objective
    data = dict()

    if carbon_sources is None:
        c_input = find_carbon_sources(model)
    else:
        c_input = model.reactions.get_by_any(carbon_sources)

    if c_input is None:
        data['carbon_source'] = None
    elif hasattr(c_input, 'id'):
        data['carbon_source'] = c_input.id
    else:
        data['carbon_source'] = ', '.join(rxn.id for rxn in c_input)

    threshold = normalize_cutoff(model, threshold)

    size = points ** len(reactions)

    for direction in ('minimum', 'maximum'):
        data['flux_{}'.format(direction)] = full(size, nan, dtype=float)
        data['carbon_yield_{}'.format(direction)] = full(
            size, nan, dtype=float)
        data['mass_yield_{}'.format(direction)] = full(
            size, nan, dtype=float)

    grid = pd.DataFrame(data)

    with model:
        model.objective = objective
        objective_reactions = list(sutil.linear_reaction_coefficients(model))

        if len(objective_reactions) != 1:
            raise ValueError('cannot calculate yields for objectives with '
                             'multiple reactions')
        c_output = objective_reactions[0]
        min_max = fva(model, reactions, fraction_of_optimum=0)
        min_max[min_max.abs() < threshold] = 0.0
        points = list(product(*[
            linspace(min_max.at[rxn.id, "minimum"],
                     min_max.at[rxn.id, "maximum"],
                     points, endpoint=True) for rxn in reactions]))
        tmp = pd.DataFrame(points, columns=[rxn.id for rxn in reactions])
        grid = pd.concat([grid, tmp], axis=1, copy=False)
        add_envelope(model, reactions, grid, c_input, c_output, threshold)

    return grid