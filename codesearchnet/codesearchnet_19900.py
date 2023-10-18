def proto_0304(theABF):
    """protocol: repeated IC steps."""

    abf=ABF(theABF)
    abf.log.info("analyzing as repeated current-clamp step")

    # prepare for AP analysis
    ap=AP(abf)

    # calculate rest potential
    avgVoltagePerSweep = [];
    times = []
    for sweep in abf.setsweeps():
        avgVoltagePerSweep.append(abf.average(0,3))
        times.append(abf.sweepStart/60)

    # detect only step APs
    M1,M2=3.15,4.15
    ap.detect_time1, ap.detect_time2 = M1,M2
    ap.detect()
    apsPerSweepCos=[len(x) for x in ap.get_bySweep()]

    # detect all APs
    M1,M2=0,10
    ap.detect_time1, ap.detect_time2 = M1,M2
    ap.detect()
    apsPerSweepRamp=[len(x) for x in ap.get_bySweep()]

    # make the plot of APs and stuff
    plt.figure(figsize=(8,8))

    plt.subplot(311)
    plt.grid(ls='--',alpha=.5)
    plt.plot(times,avgVoltagePerSweep,'.-')
    plt.ylabel("Rest Potential (mV)")
    comment_lines(abf)

    plt.subplot(312)
    plt.grid(ls='--',alpha=.5)
    plt.plot(times,apsPerSweepCos,'.-')
    plt.ylabel("APs in Step (#)")
    comment_lines(abf)

    plt.subplot(313)
    plt.grid(ls='--',alpha=.5)
    plt.plot(times,apsPerSweepRamp,'.-')
    plt.ylabel("APs in Sweep (#)")
    comment_lines(abf)

    plt.tight_layout()

    frameAndSave(abf,"cos ramp")
    plt.close('all')