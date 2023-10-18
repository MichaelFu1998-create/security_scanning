def scaled_figsize(X, figsize=None, h_pad=None, v_pad=None):
    """
    Given an array *X*, determine a good size for the figure to be by shrinking it to fit within *figsize*. If not specified, shrinks to fit the figsize specified by the current :attr:`matplotlib.rcParams`.

    .. versionadded:: 1.3
    """
    if figsize is None:
        figsize = _mpl.rcParams['figure.figsize']

    # ======================================
    # Find the height and width
    # ======================================
    width, height = _np.shape(X)
    
    ratio = width / height
    
    # ======================================
    # Find how to rescale the figure
    # ======================================
    if ratio > figsize[0]/figsize[1]:
        figsize[1] = figsize[0] / ratio
    else:
        figsize[0] = figsize[1] * ratio
    
    return figsize