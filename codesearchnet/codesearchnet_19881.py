def IV(abf,T1,T2,plotToo=True,color='b'):
    """
    Given two time points (seconds) return IV data.
    Optionally plots a fancy graph (with errorbars)
    Returns [[AV],[SD]] for the given range.
    """
    rangeData=abf.average_data([[T1,T2]]) #get the average data per sweep
    AV,SD=rangeData[:,0,0],rangeData[:,0,1] #separate by average and SD
    Xs=abf.clampValues(T1) #get clamp values at time point T1
    if plotToo:
        new(abf) #do this so it's the right shape and size

        # plot the original sweep
        pylab.subplot(221)
        pylab.title("sweep data")
        pylab.xlabel("time (s)")
        pylab.ylabel("Measurement (%s)"%abf.units)
        sweep(abf,'all',protocol=False)
        pylab.axis([None,None,np.min(rangeData)-50,np.max(rangeData)+50])
        pylab.axvspan(T1,T2,alpha=.1,color=color) #share measurement region
        pylab.margins(0,.1)

        # plot the data zoomed in
        pylab.subplot(223)
        pylab.title("measurement region")
        pylab.xlabel("time (s)")
        pylab.ylabel("Measurement (%s)"%abf.units)
        sweep(abf,'all',protocol=False)
        pylab.axis([T1-.05,T2+.05,np.min(rangeData)-50,np.max(rangeData)+50])
        pylab.axvspan(T1,T2,alpha=.1,color=color) #share measurement region
        pylab.margins(0,.1)

        # plot the protocol
        pylab.subplot(222)
        pylab.title("protocol")
        pylab.xlabel("time (s)")
        pylab.ylabel("Command (%s)"%abf.unitsCommand)
        sweep(abf,'all',protocol=True)
        pylab.axvspan(T1,T2,alpha=.1,color=color) #share measurement region
        pylab.margins(0,.1)

        # plot the I/V
        pylab.subplot(224)
        pylab.grid(alpha=.5)
        pylab.title("command / measure relationship")
        pylab.xlabel("Command (%s)"%abf.unitsCommand)
        pylab.ylabel("Measurement (%s)"%abf.units)
        pylab.errorbar(Xs,AV,SD,capsize=0,marker='.',color=color)
        if abf.units=="pA":
            pylab.axhline(0,alpha=.5,lw=2,color='r',ls="--")
            pylab.axvline(-70,alpha=.5,lw=2,color='r',ls="--")
        else:
            pylab.axhline(-70,alpha=.5,lw=2,color='r',ls="--")
            pylab.axvline(0,alpha=.5,lw=2,color='r',ls="--")
        pylab.margins(.1,.1)
    annotate(abf)
    return AV,SD