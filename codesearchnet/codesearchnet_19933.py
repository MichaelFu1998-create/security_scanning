def proto_02_01_MT70(abf=exampleABF):
    """repeated membrane tests."""
    standard_overlayWithAverage(abf)
    swhlab.memtest.memtest(abf)
    swhlab.memtest.checkSweep(abf)
    swhlab.plot.save(abf,tag='check',resize=False)