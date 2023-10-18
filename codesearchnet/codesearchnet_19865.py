def check_AP_group(abf=exampleABF,sweep=0):
    """
    after running detect() and abf.SAP is populated, this checks it.
    """
    abf.setSweep(sweep)
    swhlab.plot.new(abf,title="sweep %d (%d pA)"%(abf.currentSweep,abf.protoSeqY[1]))
    swhlab.plot.sweep(abf)
    SAP=cm.matrixToDicts(abf.SAP[sweep])
    if "T1" in SAP.keys():
        T1=SAP["T1"]
        T2=SAP["T2"]
        pylab.axvspan(T1/abf.rate,T2/abf.rate,color='r',alpha=.1)
    else:
        T1=0
        T2=abf.sweepLength
    swhlab.plot.annotate(abf)
    pylab.tight_layout()
    pylab.subplots_adjust(right=0.6)
    pylab.annotate(cm.msgDict(SAP),(.71,.95),ha='left',va='top',
                   weight='bold',family='monospace',
                   xycoords='figure fraction',size=12,color='g')
    pylab.axis([T1-.05,T2+.05,None,None])