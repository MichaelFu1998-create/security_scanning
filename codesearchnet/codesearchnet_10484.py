def plot_centres(array, centres, units, kpc_per_arcsec, zoom_offset_arcsec):
    """Plot the (y,x) centres (e.g. of a mass profile) on the array as an 'x'.

    Parameters
    -----------
    array : data.array.scaled_array.ScaledArray
        The 2D array of data which is plotted.
    centres : [[tuple]]
        The list of centres; centres in the same list entry are colored the same.
    units : str
        The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
    kpc_per_arcsec : float or None
        The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
    """
    if centres is not None:

        colors = itertools.cycle(["m", "y", "r", "w", "c", "b", "g", "k"])

        for centres_of_galaxy in centres:
            color = next(colors)
            for centre in centres_of_galaxy:

                if zoom_offset_arcsec is not None:
                    centre -= zoom_offset_arcsec

                centre_units = convert_grid_units(array=array, grid_arcsec=centre, units=units,
                                                  kpc_per_arcsec=kpc_per_arcsec)
                plt.scatter(y=centre_units[0], x=centre_units[1], s=300, c=color, marker='x')