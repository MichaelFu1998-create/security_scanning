def _addBase(self, position, xlabel=None, ylabel=None):
    """ Adds a subplot to the plot's figure at specified position.

    @param position A 3-digit number. The first two digits define a 2D grid
            where subplots may be added. The final digit specifies the nth grid
            location for the added subplot
    @param xlabel text to be displayed on the x-axis
    @param ylabel text to be displayed on the y-axis
    @returns (matplotlib.Axes) Axes instance
    """
    ax = self._fig.add_subplot(position)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax