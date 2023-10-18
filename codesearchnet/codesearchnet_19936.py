def proto_04_01_MTmon70s2(abf=exampleABF):
    """repeated membrane tests, likely with drug added. Maybe IPSCs."""
    standard_inspect(abf)
    swhlab.memtest.memtest(abf)
    swhlab.memtest.checkSweep(abf)
    swhlab.plot.save(abf,tag='check',resize=False)
    swhlab.memtest.plot_standard4(abf)
    swhlab.plot.save(abf,tag='memtests')