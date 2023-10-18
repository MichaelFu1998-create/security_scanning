def find_carbon_sources(model):
    """
    Find all active carbon source reactions.

    Parameters
    ----------
    model : Model
        A genome-scale metabolic model.

    Returns
    -------
    list
       The medium reactions with carbon input flux.

    """

    try:
        model.slim_optimize(error_value=None)
    except OptimizationError:
        return []

    reactions = model.reactions.get_by_any(list(model.medium))
    reactions_fluxes = [
        (rxn, total_components_flux(rxn.flux, reaction_elements(rxn),
                                    consumption=True)) for rxn in reactions]
    return [rxn for rxn, c_flux in reactions_fluxes if c_flux > 0]