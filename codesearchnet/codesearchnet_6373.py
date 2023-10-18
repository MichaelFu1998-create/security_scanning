def assess_products(model, reaction, flux_coefficient_cutoff=0.001,
                    solver=None):
    """Assesses whether the model has the capacity to absorb the products of
    a reaction at a given flux rate.

    Useful for identifying which components might be blocking a reaction
    from achieving a specific flux rate.

    Deprecated: use assess_component instead

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
        True if the model has the capacity to absorb all the reaction
        products being simultaneously given the specified cutoff.   False,
        if the model has the capacity to absorb each individual product but
        not all products at the required level simultaneously.   Otherwise a
        dictionary of the required and the capacity fluxes for each product
        that is not absorbed in sufficient quantities.

    """
    warn('use assess_component instead', DeprecationWarning)
    return assess_component(model, reaction, 'products',
                            flux_coefficient_cutoff, solver)