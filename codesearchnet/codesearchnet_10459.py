def setup_figure(figsize, as_subplot):
    """Setup a figure for plotting an image.

    Parameters
    -----------
    figsize : (int, int)
        The size of the figure in (rows, columns).
    as_subplot : bool
        If the figure is a subplot, the setup_figure function is omitted to ensure that each subplot does not create a \
        new figure and so that it can be output using the *output_subplot_array* function.
    """
    if not as_subplot:
        fig = plt.figure(figsize=figsize)
        return fig