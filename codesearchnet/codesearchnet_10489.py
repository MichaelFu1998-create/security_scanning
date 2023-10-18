def plot_grid(grid_arcsec, array, units, kpc_per_arcsec, pointsize, zoom_offset_arcsec):
    """Plot a grid of points over the array of data on the figure.

     Parameters
     -----------.
     grid_arcsec : ndarray or data.array.grids.RegularGrid
         A grid of (y,x) coordinates in arc-seconds which may be plotted over the array.
     array : data.array.scaled_array.ScaledArray
        The 2D array of data which is plotted.
     units : str
         The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
     kpc_per_arcsec : float or None
         The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
     grid_pointsize : int
         The size of the points plotted to show the grid.
     """
    if grid_arcsec is not None:

        if zoom_offset_arcsec is not None:
            grid_arcsec -= zoom_offset_arcsec

        grid_units = convert_grid_units(grid_arcsec=grid_arcsec, array=array, units=units,
                                        kpc_per_arcsec=kpc_per_arcsec)

        plt.scatter(y=np.asarray(grid_units[:, 0]), x=np.asarray(grid_units[:, 1]), s=pointsize, c='k')