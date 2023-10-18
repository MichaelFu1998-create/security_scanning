def get_normalization_scale(norm, norm_min, norm_max, linthresh, linscale):
    """Get the normalization scale of the colormap. This will be scaled based on the input min / max normalization \
    values.

    For a 'symmetric_log' colormap, linthesh and linscale also change the colormap.

    If norm_min / norm_max are not supplied, the minimum / maximum values of the array of data are used.

    Parameters
    -----------
    array : data.array.scaled_array.ScaledArray
        The 2D array of data which is plotted.
    norm_min : float or None
        The minimum array value the colormap map spans (all values below this value are plotted the same color).
    norm_max : float or None
        The maximum array value the colormap map spans (all values above this value are plotted the same color).
    linthresh : float
        For the 'symmetric_log' colormap normalization ,this specifies the range of values within which the colormap \
        is linear.
    linscale : float
        For the 'symmetric_log' colormap normalization, this allowws the linear range set by linthresh to be stretched \
        relative to the logarithmic range.
    """
    if norm is 'linear':
        return colors.Normalize(vmin=norm_min, vmax=norm_max)
    elif norm is 'log':
        if norm_min == 0.0:
            norm_min = 1.e-4
        return colors.LogNorm(vmin=norm_min, vmax=norm_max)
    elif norm is 'symmetric_log':
        return colors.SymLogNorm(linthresh=linthresh, linscale=linscale, vmin=norm_min, vmax=norm_max)
    else:
        raise exc.PlottingException('The normalization (norm) supplied to the plotter is not a valid string (must be '
                                     'linear | log | symmetric_log')