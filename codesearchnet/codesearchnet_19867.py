def check_sweep(abf,sweep=None,dT=.1):
    """Plotting for an eyeball check of AP detection in the given sweep."""
    if abf.APs is None:
        APs=[]
    else:
        APs=cm.matrixToDicts(abf.APs)

    if sweep is None or len(sweep)==0: #find the first sweep with >5APs in it
        for sweepNum in range(abf.sweeps):
            foundInThisSweep=0
            for AP in APs:
                if AP["sweep"]==sweepNum:
                    foundInThisSweep+=1
                if foundInThisSweep>=5:
                    break
        sweep=sweepNum
    abf.setSweep(sweep)
    Y=abf.dataY

    dI = int(dT/1000*abf.rate) #dI is dT/rate
    dY = (Y[dI:]-Y[:-dI])*(abf.rate/1000/dI) #now in V/S

    pylab.figure(figsize=(12,6))
    ax=pylab.subplot(211)
    pylab.title("sweep %d"%abf.currentSweep)
    pylab.ylabel("membrane potential (mV)")
    pylab.plot(Y,'-',alpha=.8)
    for AP in APs:
        if not AP["sweep"]==sweep:
            continue
        pylab.axvline(AP["sweepI"],alpha=.2,color='r')
        pylab.plot(AP["peakI"],AP["peak"],'.',alpha=.5,ms=20,color='r')
        pylab.plot(AP["thresholdI"],AP["threshold"],'.',alpha=.5,ms=20,color='c')
        pylab.plot([AP["AHPI"],AP["AHPreturnI"]],
                    [AP["AHP"],AP["AHPreturn"]],
                    '-',alpha=.2,ms=20,color='b',lw=7)
        pylab.plot([AP["halfwidthI1"],AP["halfwidthI2"]],
                   [AP["halfwidthPoint"],AP["halfwidthPoint"]],
                   '-',lw=5,alpha=.5,color='g')

    pylab.subplot(212,sharex=ax)
    pylab.ylabel("velocity (V/S)")
    pylab.xlabel("data points (%.02f kHz)"%(abf.rate/1000))
    pylab.plot(dY,'-',alpha=.8)
    pylab.margins(0,.1)
    for AP in APs:
        if not AP["sweep"]==sweep:
            continue
        pylab.axvline(AP["sweepI"],alpha=.2,color='r')
        pylab.plot(AP["upslopeI"],AP["upslope"],'.',alpha=.5,ms=20,color='g')
        pylab.plot(AP["downslopeI"],AP["downslope"],'.',alpha=.5,ms=20,color='g')
        pylab.axis([APs[0]["sweepI"]-1000,APs[-1]["sweepI"]+1000,None,None])