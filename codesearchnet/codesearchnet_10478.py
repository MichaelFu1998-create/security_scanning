def get_extent(array, units, kpc_per_arcsec, xticks_manual, yticks_manual):
    """Get the extent of the dimensions of the array in the units of the figure (e.g. arc-seconds or kpc).

    This is used to set the extent of the array and thus the y / x axis limits.

    Parameters
    -----------
    array : data.array.scaled_array.ScaledArray
        The 2D array of data which is plotted.
    units : str
        The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
    kpc_per_arcsec : float
        The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
    xticks_manual :  [] or None
        If input, the xticks do not use the array's default xticks but instead overwrite them as these values.
    yticks_manual :  [] or None
        If input, the yticks do not use the array's default yticks but instead overwrite them as these values.
    """
    if xticks_manual is not None and yticks_manual is not None:
        return np.asarray([xticks_manual[0], xticks_manual[3], yticks_manual[0], yticks_manual[3]])

    if units in 'pixels':
        return np.asarray([0, array.shape[1], 0, array.shape[0]])
    elif units in 'arcsec' or kpc_per_arcsec is None:
        return np.asarray([array.arc_second_minima[1], array.arc_second_maxima[1],
                           array.arc_second_minima[0], array.arc_second_maxima[0]])
    elif units in 'kpc':
        return list(map(lambda tick : tick*kpc_per_arcsec,
                        np.asarray([array.arc_second_minima[1], array.arc_second_maxima[1],
                                    array.arc_second_minima[0], array.arc_second_maxima[0]])))
    else:
        raise exc.PlottingException('The units supplied to the plotted are not a valid string (must be pixels | '
                                     'arcsec | kpc)')