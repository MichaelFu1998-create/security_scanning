def plot_origin(array, origin, units, kpc_per_arcsec, zoom_offset_arcsec):
    """Plot the (y,x) origin ofo the array's coordinates as a 'x'.
    
    Parameters
    -----------
    array : data.array.scaled_array.ScaledArray
        The 2D array of data which is plotted.
    origin : (float, float).
        The origin of the coordinate system of the array, which is plotted as an 'x' on the image if input.
    units : str
        The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
    kpc_per_arcsec : float or None
        The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
    """
    if origin is not None:

        origin_grid = np.asarray(origin)

        if zoom_offset_arcsec is not None:
            origin_grid -= zoom_offset_arcsec

        origin_units = convert_grid_units(array=array, grid_arcsec=origin_grid, units=units,
                                          kpc_per_arcsec=kpc_per_arcsec)
        plt.scatter(y=origin_units[0], x=origin_units[1], s=80, c='k', marker='x')