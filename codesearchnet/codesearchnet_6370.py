def assess(model, reaction, flux_coefficient_cutoff=0.001, solver=None):
    """Assesses production capacity.

    Assesses the capacity of the model to produce the precursors for the
    reaction and absorb the production of the reaction while the reaction is
    operating at, or above, the specified cutoff.

    Parameters
    ----------
    model : cobra.Model
        The cobra model to assess production capacity for

    reaction : reaction identifier or cobra.Reaction
        The reaction to assess

    flux_coefficient_cutoff :  float
        The minimum flux that reaction must carry to be considered active.

    solver : basestring
        Solver name. If None, the default solver will be used.

    Returns
    -------
    bool or dict
        True if the model can produce the precursors and absorb the products
        for the reaction operating at, or above, flux_coefficient_cutoff.
        Otherwise, a dictionary of {'precursor': Status, 'product': Status}.
        Where Status is the results from assess_precursors and
        assess_products, respectively.

    """
    reaction = model.reactions.get_by_any(reaction)[0]
    with model as m:
        m.objective = reaction
        if _optimize_or_value(m, solver=solver) >= flux_coefficient_cutoff:
            return True
        else:
            results = dict()
            results['precursors'] = assess_component(
                model, reaction, 'reactants', flux_coefficient_cutoff)
            results['products'] = assess_component(
                model, reaction, 'products', flux_coefficient_cutoff)
            return results