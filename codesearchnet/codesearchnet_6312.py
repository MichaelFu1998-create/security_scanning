def _as_medium(exchanges, tolerance=1e-6, exports=False):
    """Convert a solution to medium.

    Arguments
    ---------
    exchanges : list of cobra.reaction
        The exchange reactions to consider.
    tolerance : positive double
        The absolute tolerance for fluxes. Fluxes with an absolute value
        smaller than this number will be ignored.
    exports : bool
        Whether to return export fluxes as well.

    Returns
    -------
    pandas.Series
        The "medium", meaning all active import fluxes in the solution.
    """
    LOGGER.debug("Formatting medium.")
    medium = pd.Series()
    for rxn in exchanges:
        export = len(rxn.reactants) == 1
        flux = rxn.flux
        if abs(flux) < tolerance:
            continue
        if export:
            medium[rxn.id] = -flux
        elif not export:
            medium[rxn.id] = flux
    if not exports:
        medium = medium[medium > 0]

    return medium