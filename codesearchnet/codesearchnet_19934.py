def proto_02_02_IVdual(abf=exampleABF):
    """dual I/V steps in VC mode, one from -70 and one -50."""

    av1,sd1=swhlab.plot.IV(abf,.7,1,True,'b')
    swhlab.plot.save(abf,tag='iv1')
    a2v,sd2=swhlab.plot.IV(abf,2.2,2.5,True,'r')
    swhlab.plot.save(abf,tag='iv2')

    swhlab.plot.sweep(abf,'all')
    pylab.axis([None,None,min(av1)-50,max(av1)+50])
    swhlab.plot.save(abf,tag='overlay')