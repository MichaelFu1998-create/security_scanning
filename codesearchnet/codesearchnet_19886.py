def new(ABF,forceNewFigure=False,title=None,xlabel=None,ylabel=None):
    """
    makes a new matplotlib figure with default dims and DPI.
    Also labels it with pA or mV depending on ABF.
    """
    if len(pylab.get_fignums()) and forceNewFigure==False:
        #print("adding to existing figure")
        return
    pylab.figure(figsize=(8,6))
    pylab.grid(alpha=.5)
    pylab.title(ABF.ID)
    pylab.ylabel(ABF.units)
    pylab.xlabel("seconds")
    if xlabel:
        pylab.xlabel(xlabel)
    if ylabel:
        pylab.ylabel(ylabel)
    if title:
        pylab.title(title)
    annotate(ABF)