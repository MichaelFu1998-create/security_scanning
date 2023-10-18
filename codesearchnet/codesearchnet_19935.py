def proto_02_03_IVfast(abf=exampleABF):
    """fast sweeps, 1 step per sweep, for clean IV without fast currents."""
    av1,sd1=swhlab.plot.IV(abf,.6,.9,True)
    swhlab.plot.save(abf,tag='iv1')
    Xs=abf.clampValues(.6) #generate IV clamp values
    abf.saveThing([Xs,av1],'iv')