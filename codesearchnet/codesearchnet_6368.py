def total_components_flux(flux, components, consumption=True):
    """
    Compute the total components consumption or production flux.

    Parameters
    ----------
    flux : float
        The reaction flux for the components.
    components : list
        List of stoichiometrically weighted components.
    consumption : bool, optional
        Whether to sum up consumption or production fluxes.

    """

    direction = 1 if consumption else -1
    c_flux = [elem * flux * direction for elem in components]

    return sum([flux for flux in c_flux if flux > 0])