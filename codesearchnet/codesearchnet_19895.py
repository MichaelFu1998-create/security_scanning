def proto_gain(theABF,stepSize=25,startAt=-100):
    """protocol: gain function of some sort. step size and start at are pA."""
    abf=ABF(theABF)
    abf.log.info("analyzing as an IC ramp")
    plot=ABFplot(abf)
    plot.kwargs["lw"]=.5
    plot.title=""
    currents=np.arange(abf.sweeps)*stepSize-startAt

    # AP detection
    ap=AP(abf)
    ap.detect_time1=.1
    ap.detect_time2=.7
    ap.detect()

    # stacked plot
    plt.figure(figsize=(SQUARESIZE,SQUARESIZE))

    ax1=plt.subplot(221)
    plot.figure_sweeps()

    ax2=plt.subplot(222)
    ax2.get_yaxis().set_visible(False)
    plot.figure_sweeps(offsetY=150)

    # add vertical marks to graphs:
    for ax in [ax1,ax2]:
        for limit in [ap.detect_time1,ap.detect_time2]:
            ax.axvline(limit,color='r',ls='--',alpha=.5,lw=2)

    # make stacked gain function
    ax4=plt.subplot(223)
    plt.ylabel("frequency (Hz)")
    plt.ylabel("seconds")
    plt.grid(alpha=.5)
    freqs=ap.get_bySweep("freqs")
    times=ap.get_bySweep("times")
    for i in range(abf.sweeps):
        if len(freqs[i]):
            plt.plot(times[i][:-1],freqs[i],'-',alpha=.5,lw=2,
                     color=plot.getColor(i/abf.sweeps))

    # make gain function graph
    ax4=plt.subplot(224)
    ax4.grid(alpha=.5)
    plt.plot(currents,ap.get_bySweep("median"),'b.-',label="median")
    plt.plot(currents,ap.get_bySweep("firsts"),'g.-',label="first")
    plt.xlabel("applied current (pA)")
    plt.legend(loc=2,fontsize=10)
    plt.axhline(40,color='r',alpha=.5,ls="--",lw=2)
    plt.margins(.02,.1)

    # save it
    plt.tight_layout()
    frameAndSave(abf,"AP Gain %d_%d"%(startAt,stepSize))
    plt.close('all')

    # make a second figure that just shows every sweep up to the first AP
    plt.figure(figsize=(SQUARESIZE,SQUARESIZE))
    plt.grid(alpha=.5)
    plt.ylabel("Membrane Potential (mV)")
    plt.xlabel("Time (seconds)")
    for sweep in abf.setsweeps():
        plt.plot(abf.sweepX2,abf.sweepY,color='b',alpha=.5)
        if np.max(abf.sweepY>0):
            break
    plt.tight_layout()
    plt.margins(0,.1)

    plt.axis([0,1,None,None])
    plt.title("%d pA Steps from Rest"%stepSize)
    frameAndSave(abf,"voltage response fromRest",closeWhenDone=False)
    plt.axis([1.5,2.5,None,None])
    plt.title("%d pA Steps from %d pA"%(stepSize,startAt))
    frameAndSave(abf,"voltage response hyperpol",closeWhenDone=False)
    plt.close('all')