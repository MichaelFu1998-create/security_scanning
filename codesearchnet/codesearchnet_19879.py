def values_above_sweep(abf,dataI,dataY,ylabel="",useFigure=None):
    """
    To make plots like AP frequency over original trace.
    dataI=[i] #the i of the sweep
    dataY=[1.234] #something like inst freq
    """
    xOffset = abf.currentSweep*abf.sweepInterval
    if not useFigure: #just passing the figure makes it persistant!
        pylab.figure(figsize=(8,6))

    ax=pylab.subplot(221)
    pylab.grid(alpha=.5)
    if len(dataI):
        pylab.plot(abf.dataX[dataI],dataY,'.',ms=10,alpha=.5,
                   color=abf.colormap[abf.currentSweep])
    pylab.margins(0,.1)
    pylab.ylabel(ylabel)

    pylab.subplot(223,sharex=ax)
    pylab.grid(alpha=.5)
    pylab.plot(abf.dataX,abf.dataY,color=abf.colormap[abf.currentSweep],alpha=.5)
    pylab.ylabel("raw data (%s)"%abf.units)

    ax2=pylab.subplot(222)
    pylab.grid(alpha=.5)
    if len(dataI):
        pylab.plot(abf.dataX[dataI]+xOffset,dataY,'.',ms=10,alpha=.5,
                   color=abf.colormap[abf.currentSweep])
    pylab.margins(0,.1)
    pylab.ylabel(ylabel)

    pylab.subplot(224,sharex=ax2)
    pylab.grid(alpha=.5)
    pylab.plot(abf.dataX+xOffset,abf.dataY,color=abf.colormap[abf.currentSweep])
    pylab.ylabel("raw data (%s)"%abf.units)

    pylab.tight_layout()