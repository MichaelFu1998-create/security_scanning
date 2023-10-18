def proto_VC_50_MT_IV(abf=exampleABF):
    """combination of membrane test and IV steps."""
    swhlab.memtest.memtest(abf) #do membrane test on every sweep
    swhlab.memtest.checkSweep(abf) #see all MT values
    swhlab.plot.save(abf,tag='02-check',resize=False)

    av1,sd1=swhlab.plot.IV(abf,1.2,1.4,True,'b')
    swhlab.plot.save(abf,tag='iv')
    Xs=abf.clampValues(1.2) #generate IV clamp values
    abf.saveThing([Xs,av1],'01_iv')