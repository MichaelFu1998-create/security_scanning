def analyze(fname=False,save=True,show=None):
    """given a filename or ABF object, try to analyze it."""
    if fname and os.path.exists(fname.replace(".abf",".rst")):
        print("SKIPPING DUE TO RST FILE")
        return
    swhlab.plotting.core.IMAGE_SAVE=save
    if show is None:
        if cm.isIpython():
            swhlab.plotting.core.IMAGE_SHOW=True
        else:
            swhlab.plotting.core.IMAGE_SHOW=False
    #swhlab.plotting.core.IMAGE_SHOW=show
    abf=ABF(fname) # ensure it's a class
    print(">>>>> PROTOCOL >>>>>",abf.protocomment)
    runFunction="proto_unknown"
    if "proto_"+abf.protocomment in globals():
        runFunction="proto_"+abf.protocomment
    abf.log.debug("running %s()"%(runFunction))
    plt.close('all') # get ready
    globals()[runFunction](abf) # run that function
    try:
        globals()[runFunction](abf) # run that function
    except:
        abf.log.error("EXCEPTION DURING PROTOCOL FUNCTION")
        abf.log.error(sys.exc_info()[0])
        return "ERROR"
    plt.close('all') # clean up
    return "SUCCESS"