def inspectABF(abf=exampleABF,saveToo=False,justPlot=False):
    """May be given an ABF object or filename."""
    pylab.close('all')
    print(" ~~ inspectABF()")
    if type(abf) is str:
        abf=swhlab.ABF(abf)
    swhlab.plot.new(abf,forceNewFigure=True)
    if abf.sweepInterval*abf.sweeps<60*5: #shorter than 5 minutes
        pylab.subplot(211)
        pylab.title("%s [%s]"%(abf.ID,abf.protoComment))
        swhlab.plot.sweep(abf,'all')
        pylab.subplot(212)
        swhlab.plot.sweep(abf,'all',continuous=True)
        swhlab.plot.comments(abf)
    else:
        print(" -- plotting as long recording")
        swhlab.plot.sweep(abf,'all',continuous=True,minutes=True)
        swhlab.plot.comments(abf,minutes=True)
        pylab.title("%s [%s]"%(abf.ID,abf.protoComment))
    swhlab.plot.annotate(abf)
    if justPlot:
        return
    if saveToo:
        path=os.path.split(abf.fname)[0]
        basename=os.path.basename(abf.fname)
        pylab.savefig(os.path.join(path,"_"+basename.replace(".abf",".png")))
    pylab.show()
    return