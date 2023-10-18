def sweep(ABF,sweep=None,rainbow=True,alpha=None,protocol=False,color='b',
               continuous=False,offsetX=0,offsetY=0,minutes=False,
               decimate=None,newFigure=False):
    """
    Load a particular sweep then plot it.
    If sweep is None or False, just plot current dataX/dataY.
    If rainbow, it'll make it color coded prettily.
    """
    if len(pylab.get_fignums())==0 or newFigure:
        new(ABF,True)
    if offsetY>0:
        pylab.grid(None)

    # figure which sweeps to plot
    if sweep is None:
        sweeps=[ABF.currentSweep]
        if not ABF.currentSweep:
            sweeps=[0]
    elif sweep=="all":
        sweeps=range(0,ABF.sweeps)
    elif type(sweep) in [int,float]:
        sweeps=[int(sweep)]
    elif type(sweep) is list:
        sweeps=sweep
    else:
        print("DONT KNOW WHAT TO DO WITH THIS SWEEPS!!!\n",type(sweep),sweep)

    #figure out offsets:
    if continuous:
        offsetX=ABF.sweepInterval

    # determine the colors to use
    colors=[color]*len(sweeps) #detault to blue
    if rainbow and len(sweeps)>1:
        for i in range(len(sweeps)):
            colors[i]=ABF.colormap[i]
    if alpha is None and len(sweeps)==1:
        alpha=1
    if rainbow and alpha is None:
        alpha=.5

    # correct for alpha
    if alpha is None:
        alpha=1

    # conversion to minutes?
    if minutes == False:
        minutes=1
    else:
        minutes=60
        pylab.xlabel("minutes")

    ABF.decimateMethod=decimate
    # do the plotting of each sweep
    for i in range(len(sweeps)):
        ABF.setSweep(sweeps[i])
        if protocol:
            pylab.plot((np.array(ABF.protoX)/ABF.rate+offsetX*i)/minutes,
                       ABF.protoY+offsetY*i,
                       alpha=alpha,color=colors[i])
        else:
            pylab.plot((ABF.dataX+offsetX*i)/minutes,
                       ABF.dataY+offsetY*i,alpha=alpha,color=colors[i])
    ABF.decimateMethod=None
    pylab.margins(0,.02)