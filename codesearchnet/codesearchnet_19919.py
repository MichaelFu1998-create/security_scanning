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

    # start by lowpass filtering (1 direction)
#    Klpf=kernel_gaussian(size=abf.pointsPerMs*10,forwardOnly=True)
#    Ylpf=np.convolve(Yorig,Klpf,mode='same')
#    Y=Ylpf # commit

    Kmb=kernel_gaussian(size=abf.pointsPerMs*10,forwardOnly=True)
    Ymb=np.convolve(Yorig,Kmb,mode='same')
    Y=Yorig-Ymb # commit

    #Y1=np.copy(Y)
    #Y[np.where(Y>0)[0]]=np.power(Y,2)
    #Y[np.where(Y<0)[0]]=-np.power(Y,2)

    # event detection
    thresh=5 # threshold for an event
    hitPos=np.where(Y>thresh)[0] # area above the threshold
    hitNeg=np.where(Y<-thresh)[0] # area below the threshold
    hitPos=np.concatenate((hitPos,[len(Y)-1])) # helps with the diff() coming up
    hitNeg=np.concatenate((hitNeg,[len(Y)-1])) # helps with the diff() coming up
    hitsPos=hitPos[np.where(np.abs(np.diff(hitPos))>10)[0]] # time point of EPSC
    hitsNeg=hitNeg[np.where(np.abs(np.diff(hitNeg))>10)[0]] # time point of IPSC
    hitsNeg=hitsNeg[1:] # often the first one is in error
    #print(hitsNeg[0])

    if plotToo:
        plt.figure(figsize=(10,5))
        ax1=plt.subplot(211)
        plt.title("sweep %d: detected %d IPSCs (red) and %d EPSCs (blue)"%(sweep,len(hitsPos),len(hitsNeg)))
        plt.ylabel("delta pA")
        plt.grid()

        plt.plot(X,Yorig,color='k',alpha=.5)
        for hit in hitsPos:
            plt.plot(X[hit],Yorig[hit]+20,'r.',ms=20,alpha=.5)
        for hit in hitsNeg:
            plt.plot(X[hit],Yorig[hit]-20,'b.',ms=20,alpha=.5)
        plt.margins(0,.1)

        plt.subplot(212,sharex=ax1)
        plt.title("moving gaussian baseline subtraction used for threshold detection")
        plt.ylabel("delta pA")
        plt.grid()
        plt.axhline(thresh,color='r',ls='--',alpha=.5,lw=3)
        plt.axhline(-thresh,color='r',ls='--',alpha=.5,lw=3)
        plt.plot(X,Y,color='b',alpha=.5)

        plt.axis([X[0],X[-1],-thresh*1.5,thresh*1.5])
        plt.tight_layout()
        if type(plotToo) is str and os.path.isdir(plotToo):
            print('saving %s/%05d.jpg'%(plotToo,sweep))
            plt.savefig(plotToo+"/%05d.jpg"%sweep)
        else:
            plt.show()
        plt.close('all')

    return [len(hitsPos),len(hitsNeg)]