def proto_01_01_HP010(abf=exampleABF):
    """hyperpolarization step. Use to calculate tau and stuff."""
    swhlab.memtest.memtest(abf) #knows how to do IC memtest
    swhlab.memtest.checkSweep(abf) #lets you eyeball check how it did
    swhlab.plot.save(abf,tag="tau")