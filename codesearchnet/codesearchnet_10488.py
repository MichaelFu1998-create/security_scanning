def plot_points(points_arcsec, array, units, kpc_per_arcsec, pointsize, zoom_offset_arcsec):
    """Plot a set of points over the array of data on the figure.

    Parameters
    -----------
    positions : [[]]
        Lists of (y,x) coordinates on the image which are plotted as colored dots, to highlight specific pixels.
    array : data.array.scaled_array.ScaledArray
        The 2D array of data which is plotted.
    units : str
        The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
    kpc_per_arcsec : float or None
        The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
    pointsize : int
        The size of the points plotted to show the input positions.
    """
    if points_arcsec is not None:
        points_arcsec = list(map(lambda position_set: np.asarray(position_set), points_arcsec))
        point_colors = itertools.cycle(["m", "y", "r", "w", "c", "b", "g", "k"])
        for point_set_arcsec in points_arcsec:

            if zoom_offset_arcsec is not None:
                point_set_arcsec -= zoom_offset_arcsec

            point_set_units = convert_grid_units(array=array, grid_arcsec=point_set_arcsec, units=units,
                                                 kpc_per_arcsec=kpc_per_arcsec)
            plt.scatter(y=point_set_units[:,0], x=point_set_units[:,1], color=next(point_colors), s=pointsize)