def proto_avgRange(theABF,m1=None,m2=None):
    """experiment: generic VC time course experiment."""

    abf=ABF(theABF)
    abf.log.info("analyzing as a fast IV")
    if m1 is None:
        m1=abf.sweepLength
    if m2 is None:
        m2=abf.sweepLength

    I1=int(abf.pointsPerSec*m1)
    I2=int(abf.pointsPerSec*m2)

    Ts=np.arange(abf.sweeps)*abf.sweepInterval
    Yav=np.empty(abf.sweeps)*np.nan # average
    Ysd=np.empty(abf.sweeps)*np.nan # standard deviation
    #Yar=np.empty(abf.sweeps)*np.nan # area

    for sweep in abf.setsweeps():
        Yav[sweep]=np.average(abf.sweepY[I1:I2])
        Ysd[sweep]=np.std(abf.sweepY[I1:I2])
        #Yar[sweep]=np.sum(abf.sweepY[I1:I2])/(I2*I1)-Yav[sweep]

    plot=ABFplot(abf)
    plt.figure(figsize=(SQUARESIZE*2,SQUARESIZE/2))

    plt.subplot(131)
    plot.title="first sweep"
    plot.figure_sweep(0)
    plt.title("First Sweep\n(shaded measurement range)")
    plt.axvspan(m1,m2,color='r',ec=None,alpha=.1)

    plt.subplot(132)
    plt.grid(alpha=.5)
    for i,t in enumerate(abf.comment_times):
        plt.axvline(t/60,color='r',alpha=.5,lw=2,ls='--')
    plt.plot(Ts/60,Yav,'.',alpha=.75)
    plt.title("Range Average\nTAGS: %s"%(", ".join(abf.comment_tags)))
    plt.ylabel(abf.units2)
    plt.xlabel("minutes")
    plt.margins(0,.1)

    plt.subplot(133)
    plt.grid(alpha=.5)
    for i,t in enumerate(abf.comment_times):
        plt.axvline(t/60,color='r',alpha=.5,lw=2,ls='--')
    plt.plot(Ts/60,Ysd,'.',alpha=.5,color='g',ms=15,mew=0)
    #plt.fill_between(Ts/60,Ysd*0,Ysd,lw=0,alpha=.5,color='g')
    plt.title("Range Standard Deviation\nTAGS: %s"%(", ".join(abf.comment_tags)))
    plt.ylabel(abf.units2)
    plt.xlabel("minutes")
    plt.margins(0,.1)
    plt.axis([None,None,0,np.percentile(Ysd,99)*1.25])

    plt.tight_layout()
    frameAndSave(abf,"sweep vs average","experiment")
    plt.close('all')