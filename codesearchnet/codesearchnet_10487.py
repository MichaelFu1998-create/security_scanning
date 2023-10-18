def plot_border(mask, should_plot_border, units, kpc_per_arcsec, pointsize, zoom_offset_pixels):
    """Plot the borders of the mask or the array on the figure.

    Parameters
    -----------t.
    mask : ndarray of data.array.mask.Mask
        The mask applied to the array, the edge of which is plotted as a set of points over the plotted array.
    should_plot_border : bool
        If a mask is supplied, its borders pixels (e.g. the exterior edge) is plotted if this is *True*.
    units : str
        The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
    kpc_per_arcsec : float or None
        The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
    border_pointsize : int
        The size of the points plotted to show the borders.
    """
    if should_plot_border and mask is not None:

        plt.gca()
        border_pixels = mask.masked_grid_index_to_pixel[mask.border_pixels]

        if zoom_offset_pixels is not None:
            border_pixels -= zoom_offset_pixels

        border_arcsec = mask.grid_pixels_to_grid_arcsec(grid_pixels=border_pixels)
        border_units = convert_grid_units(array=mask, grid_arcsec=border_arcsec, units=units,
                                          kpc_per_arcsec=kpc_per_arcsec)

        plt.scatter(y=border_units[:,0], x=border_units[:,1], s=pointsize, c='y')