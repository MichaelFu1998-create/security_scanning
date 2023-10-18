def add2DArray(self, data, position=111, xlabel=None, ylabel=None, cmap=None,
                 aspect="auto", interpolation="nearest", name=None):
    """ Adds an image to the plot's figure.

    @param data a 2D array. See matplotlib.Axes.imshow documentation.
    @param position A 3-digit number. The first two digits define a 2D grid
            where subplots may be added. The final digit specifies the nth grid
            location for the added subplot
    @param xlabel text to be displayed on the x-axis
    @param ylabel text to be displayed on the y-axis
    @param cmap color map used in the rendering
    @param aspect how aspect ratio is handled during resize
    @param interpolation interpolation method
    """
    if cmap is None:
      # The default colormodel is an ugly blue-red model.
      cmap = cm.Greys

    ax = self._addBase(position, xlabel=xlabel, ylabel=ylabel)
    ax.imshow(data, cmap=cmap, aspect=aspect, interpolation=interpolation)

    if self._show:
      plt.draw()

    if name is not None:
      if not os.path.exists("log"):
        os.mkdir("log")
      plt.savefig("log/{name}.png".format(name=name), bbox_inches="tight",
                  figsize=(8, 6), dpi=400)