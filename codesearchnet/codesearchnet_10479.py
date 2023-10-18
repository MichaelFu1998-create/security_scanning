def get_normalization_min_max(array, norm_min, norm_max):
    """Get the minimum and maximum of the normalization of the array, which sets the lower and upper limits of the \
    colormap.

    If norm_min / norm_max are not supplied, the minimum / maximum values of the array of data are used.

    Parameters
    -----------
    array : data.array.scaled_array.ScaledArray
        The 2D array of data which is plotted.
    norm_min : float or None
        The minimum array value the colormap map spans (all values below this value are plotted the same color).
    norm_max : float or None
        The maximum array value the colormap map spans (all values above this value are plotted the same color).
    """
    if norm_min is None:
        norm_min = array.min()
    if norm_max is None:
        norm_max = array.max()

    return norm_min, norm_max