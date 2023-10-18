def proto_0111(theABF):
    """protocol: IC ramp for AP shape analysis."""
    abf=ABF(theABF)
    abf.log.info("analyzing as an IC ramp")

    # AP detection
    ap=AP(abf)
    ap.detect()

    # also calculate derivative for each sweep
    abf.derivative=True

    # create the multi-plot figure
    plt.figure(figsize=(SQUARESIZE,SQUARESIZE))
    ax1=plt.subplot(221)
    plt.ylabel(abf.units2)
    ax2=plt.subplot(222,sharey=ax1)
    ax3=plt.subplot(223)
    plt.ylabel(abf.unitsD2)
    ax4=plt.subplot(224,sharey=ax3)

    # put data in each subplot
    for sweep in range(abf.sweeps):
        abf.setsweep(sweep)
        ax1.plot(abf.sweepX,abf.sweepY,color='b',lw=.25)
        ax2.plot(abf.sweepX,abf.sweepY,color='b')
        ax3.plot(abf.sweepX,abf.sweepD,color='r',lw=.25)
        ax4.plot(abf.sweepX,abf.sweepD,color='r')

    # modify axis
    for ax in [ax1,ax2,ax3,ax4]: # everything
        ax.margins(0,.1)
        ax.grid(alpha=.5)
    for ax in [ax3,ax4]: # only derivative APs
        ax.axhline(-100,color='r',alpha=.5,ls="--",lw=2)
    for ax in [ax2,ax4]: # only zoomed in APs
        ax.get_yaxis().set_visible(False)
    if len(ap.APs):
        firstAP=ap.APs[0]["T"]
        ax2.axis([firstAP-.25,firstAP+.25,None,None])
        ax4.axis([firstAP-.01,firstAP+.01,None,None])

    # show message from first AP
    if len(ap.APs):
        firstAP=ap.APs[0]
        msg="\n".join(["%s = %s"%(x,str(firstAP[x])) for x in sorted(firstAP.keys()) if not "I" in x[-2:]])
        plt.subplot(221)
        plt.gca().text(0.02, 0.98, msg, transform= plt.gca().transAxes, fontsize=10, verticalalignment='top', family='monospace')

    # save it
    plt.tight_layout()
    frameAndSave(abf,"AP shape")
    plt.close('all')