def createcolorbar(cmap, norm):
    """Create a colourbar with limits of lwr and upr"""
    cax, kw = matplotlib.colorbar.make_axes(matplotlib.pyplot.gca())
    c = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm)
    return c