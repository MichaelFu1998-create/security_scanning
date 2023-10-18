def show(closeToo=False):
    """alternative to pylab.show() that updates IPython window."""
    IPython.display.display(pylab.gcf())
    if closeToo:
        pylab.close('all')