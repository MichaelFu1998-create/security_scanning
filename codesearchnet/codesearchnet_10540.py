def convert_grid_units(grid_arcsec, units, kpc_per_arcsec):
    """Convert the grid from its input units (arc-seconds) to the input unit (e.g. retain arc-seconds) or convert to \
    another set of units (kiloparsecs).

    Parameters
    -----------
    grid_arcsec : ndarray or data.array.grids.RegularGrid
        The (y,x) coordinates of the grid in arc-seconds, in an array of shape (total_coordinates, 2).
    units : str
        The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
    kpc_per_arcsec : float
        The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
    """

    if units in 'arcsec' or kpc_per_arcsec is None:
        return grid_arcsec
    elif units in 'kpc':
        return grid_arcsec * kpc_per_arcsec