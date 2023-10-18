def analyzeSweep(abf,sweep,m1=None,m2=None,plotToo=False):
    """
    m1 and m2, if given, are in seconds.
    returns [# EPSCs, # IPSCs]
    """
    abf.setsweep(sweep)
    if m1 is None: m1=0
    else: m1=m1*abf.pointsPerSec
    if m2 is None: m2=-1
    else: m2=m2*abf.pointsPerSec

    # obtain X and Y
    Yorig=abf.sweepY[int(m1):int(m2)]
    X=np.arange(len(Yorig))/abf.pointsPerSec

    Ylpf=linear_gaussian(Yorig,sigmaSize=abf.pointsPerMs*300,forwardOnly=False)
    Yflat=Yorig-Ylpf

    EPSCs,IPSCs=[],[]

    if plotToo:
        plt.figure(figsize=(15,6))
        ax1=plt.subplot(211)
        plt.title("%s sweep %d"%(abf.ID,sweep))
        plt.grid()
        plt.plot(X,Yorig,alpha=.5)
        plt.plot(X,Ylpf,'k',alpha=.5,lw=2)
        plt.margins(0,.2)

        plt.subplot(212,sharex=ax1)
        plt.title("gaussian baseline subtraction")
        plt.grid()
        plt.plot(X,Yflat,alpha=.5)
        plt.axhline(0,color='k',lw=2,alpha=.5)

        plt.tight_layout()
        plt.show()

    # TEST GAUSS
    hist, bin_edges = np.histogram(Yflat, density=True, bins=200)
    peakPa=bin_edges[np.where(hist==max(hist))[0][0]+1]

    if plotToo:
        plt.figure()
        plt.grid()
        plt.plot(bin_edges[1:],hist,alpha=.5)
        plt.axvline(0,color='k')
        plt.axvline(peakPa,color='r',ls='--',lw=2,alpha=.5)
        plt.semilogy()
        plt.title("sweep data distribution")
        plt.ylabel("power")
        plt.xlabel("pA deviation")
        plt.show()

    return peakPa