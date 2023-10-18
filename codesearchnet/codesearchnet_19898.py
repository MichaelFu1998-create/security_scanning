def proto_0203(theABF):
    """protocol: vast IV."""
    abf=ABF(theABF)
    abf.log.info("analyzing as a fast IV")
    plot=ABFplot(abf)
    plot.title=""
    m1,m2=.7,1
    plt.figure(figsize=(SQUARESIZE,SQUARESIZE/2))

    plt.subplot(121)
    plot.figure_sweeps()
    plt.axvspan(m1,m2,color='r',ec=None,alpha=.1)

    plt.subplot(122)
    plt.grid(alpha=.5)
    Xs=np.arange(abf.sweeps)*5-110
    Ys=[]
    for sweep in range(abf.sweeps):
        abf.setsweep(sweep)
        Ys.append(abf.average(m1,m2))
    plt.plot(Xs,Ys,'.-',ms=10)
    plt.axvline(-70,color='r',ls='--',lw=2,alpha=.5)
    plt.axhline(0,color='r',ls='--',lw=2,alpha=.5)
    plt.margins(.1,.1)
    plt.xlabel("membrane potential (mV)")

    # save it
    plt.tight_layout()
    frameAndSave(abf,"fast IV")
    plt.close('all')