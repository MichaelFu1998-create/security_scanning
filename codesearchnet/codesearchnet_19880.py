def gain(abf):
    """easy way to plot a gain function."""
    Ys=np.nan_to_num(swhlab.ap.getAvgBySweep(abf,'freq'))
    Xs=abf.clampValues(abf.dataX[int(abf.protoSeqX[1]+.01)])
    swhlab.plot.new(abf,title="gain function",xlabel="command current (pA)",
                    ylabel="average inst. freq. (Hz)")
    pylab.plot(Xs,Ys,'.-',ms=20,alpha=.5,color='b')
    pylab.axhline(0,alpha=.5,lw=2,color='r',ls="--")
    pylab.margins(.1,.1)