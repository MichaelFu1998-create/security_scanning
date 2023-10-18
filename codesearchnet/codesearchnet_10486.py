def plot_mask(mask, units, kpc_per_arcsec, pointsize, zoom_offset_pixels):
    """Plot the mask of the array on the figure.

    Parameters
    -----------
    mask : ndarray of data.array.mask.Mask
        The mask applied to the array, the edge of which is plotted as a set of points over the plotted array.
    units : str
        The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
    kpc_per_arcsec : float or None
        The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
    pointsize : int
        The size of the points plotted to show the mask.
    """

    if mask is not None:

        plt.gca()
        edge_pixels = mask.masked_grid_index_to_pixel[mask.edge_pixels] + 0.5
        if zoom_offset_pixels is not None:
            edge_pixels -= zoom_offset_pixels
        edge_arcsec = mask.grid_pixels_to_grid_arcsec(grid_pixels=edge_pixels)
        edge_units = convert_grid_units(array=mask, grid_arcsec=edge_arcsec, units=units,
                                          kpc_per_arcsec=kpc_per_arcsec)

        plt.scatter(y=edge_units[:,0], x=edge_units[:,1], s=pointsize, c='k')