def proto_0303(theABF):
    """protocol: repeated IC ramps."""

    abf=ABF(theABF)
    abf.log.info("analyzing as a halorhodopsin (2s pulse)")

    # show average voltage
    proto_avgRange(theABF,0.2,1.2)
    plt.close('all')

    # show stacked sweeps
    plt.figure(figsize=(8,8))
    for sweep in abf.setsweeps():
        color='b'
        if sweep in np.array(abf.comment_sweeps,dtype=int):
            color='r'
        plt.plot(abf.sweepX2,abf.sweepY+100*sweep,color=color,alpha=.5)
    plt.margins(0,.01)
    plt.tight_layout()
    frameAndSave(abf,"IC ramps")
    plt.close('all')

    # do AP event detection
    ap=AP(abf)
    ap.detect_time1=2.3
    ap.detect_time2=8.3
    ap.detect()
    apCount=[]
    apSweepTimes=[]

    for sweepNumber,times in enumerate(ap.get_bySweep("times")):
        apCount.append(len(times))
        if len(times):
            apSweepTimes.append(times[0])
        else:
            apSweepTimes.append(0)

    # plot AP frequency vs time
    plt.figure(figsize=(8,8))

    ax1=plt.subplot(211)
    plt.grid(alpha=.4,ls='--')
    plt.plot(np.arange(len(apCount))*abf.sweepLength/60,apCount,'.-',ms=15)
    comment_lines(abf)
    plt.ylabel("AP Count")

    plt.subplot(212,sharex=ax1)
    plt.grid(alpha=.4,ls='--')
    plt.plot(np.arange(len(apCount))*abf.sweepLength/60,apSweepTimes,'.-',ms=15)
    comment_lines(abf)
    plt.ylabel("First AP Time (s)")
    plt.xlabel("Experiment Duration (minutes)")
    plt.tight_layout()
    frameAndSave(abf,"IC ramp freq")
    plt.close('all')