def addGraph(self, data, position=111, xlabel=None, ylabel=None):
    """ Adds a graph to the plot's figure.

    @param data See matplotlib.Axes.plot documentation.
    @param position A 3-digit number. The first two digits define a 2D grid
            where subplots may be added. The final digit specifies the nth grid
            location for the added subplot
    @param xlabel text to be displayed on the x-axis
    @param ylabel text to be displayed on the y-axis
    """
    ax = self._addBase(position, xlabel=xlabel, ylabel=ylabel)
    ax.plot(data)
    plt.draw()