def proto_01_13_steps025dual(abf=exampleABF):
    """IC steps. See how hyperpol. step affects things."""
    swhlab.ap.detect(abf)
    standard_groupingForInj(abf,200)

    for feature in ['freq','downslope']:
        swhlab.ap.plot_values(abf,feature,continuous=False) #plot AP info
        swhlab.plot.save(abf,tag='A_'+feature)

    f1=swhlab.ap.getAvgBySweep(abf,'freq',None,1)
    f2=swhlab.ap.getAvgBySweep(abf,'freq',1,None)
    f1=np.nan_to_num(f1)
    f2=np.nan_to_num(f2)
    Xs=abf.clampValues(abf.dataX[int(abf.protoSeqX[1]+.01)])
    swhlab.plot.new(abf,title="gain function",xlabel="command current (pA)",
                    ylabel="average inst. freq. (Hz)")
    pylab.plot(Xs,f1,'.-',ms=20,alpha=.5,label="step 1",color='b')
    pylab.plot(Xs,f2,'.-',ms=20,alpha=.5,label="step 2",color='r')
    pylab.legend(loc='upper left')
    pylab.axis([Xs[0],Xs[-1],None,None])
    swhlab.plot.save(abf,tag='gain')