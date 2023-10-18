def assess_precursors(model, reaction, flux_coefficient_cutoff=0.001,
                      solver=None):
    """Assesses the ability of the model to provide sufficient precursors for
    a reaction operating at, or beyond, the specified cutoff.

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
        True if the precursors can be simultaneously produced at the
        specified cutoff. False, if the model has the capacity to produce
        each individual precursor at the specified threshold  but not all
        precursors at the required level simultaneously. Otherwise a
        dictionary of the required and the produced fluxes for each reactant
        that is not produced in sufficient quantities.

    """
    warn('use assess_component instead', DeprecationWarning)
    return assess_component(model, reaction, 'reactants',
                            flux_coefficient_cutoff, solver)