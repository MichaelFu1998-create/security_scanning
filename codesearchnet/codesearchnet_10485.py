def plot_ellipses(fig, array, centres, axis_ratios, phis, units, kpc_per_arcsec, zoom_offset_arcsec):
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
    if centres is not None and axis_ratios is not None and phis is not None:

        colors = itertools.cycle(["m", "y", "r", "w", "c", "b", "g", "k"])

        for set_index in range(len(centres)):
            color = next(colors)
            for geometry_index in range(len(centres[set_index])):

                centre = centres[set_index][geometry_index]
                axis_ratio = axis_ratios[set_index][geometry_index]
                phi = phis[set_index][geometry_index]

                if zoom_offset_arcsec is not None:
                    centre -= zoom_offset_arcsec

                centre_units = convert_grid_units(array=array, grid_arcsec=centre, units=units,
                                                  kpc_per_arcsec=kpc_per_arcsec)

                y = 1.0
                x = 1.0*axis_ratio

                t = np.linspace(0, 2*np.pi, 100)
                plt.plot(centre_units[0] + y*np.cos(t), centre_units[1] + x*np.sin(t), color=color)