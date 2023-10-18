def detect(abf,sweep=None,threshold_upslope=50,dT=.1,saveToo=True):
    """
    An AP will be detected by a upslope that exceeds 50V/s. Analyzed too.
        if type(sweep) is int, graph int(sweep)
        if sweep==None, process all sweeps sweep.
    """
    if type(sweep) is int:
        sweeps=[sweep]
    else:
        sweeps=list(range(abf.sweeps))
    timeStart=time.clock()
    abf.APs=[None]*abf.sweeps
    abf.SAP=[None]*abf.sweeps
    for sweep in sweeps:
        abf.setSweep(sweep)
        Y=abf.dataY
        dI = int(dT/1000*abf.rate) #dI is dT/rate
        dY = (Y[dI:]-Y[:-dI])*(abf.rate/1000/dI) #now in V/S
        Is = cm.where_cross(dY,threshold_upslope) #found every putative AP (I units)
        abf.APs[sweep]=[]
        for i in range(len(Is)): #for each putative AP
            try:
                AP=analyzeAP(Y,dY,Is[i],abf.rate) #try to characterize it
                if AP:
                    AP["sweep"]=sweep
                    AP["expI"]=sweep*abf.sweepInterval*abf.rate*+AP["sweepI"]
                    AP["expT"]=sweep*abf.sweepInterval+AP["sweepT"]
                    AP["freq"]=np.nan #default
                    if len(abf.APs[sweep]):
                        AP["freq"]=1/(AP["expT"]-abf.APs[sweep][-1]["expT"])
                    if AP["freq"] is np.nan or AP["freq"]<500: #at 500Hz, assume you have a duplicate AP
                        abf.APs[sweep].append(AP)
            except:
                print(" -- AP %d of %d excluded from analysis..."%(i+1,len(Is)))
                #print("!!! AP CRASH !!!")
                #print(traceback.format_exc())
        analyzeAPgroup(abf) #now that APs are known, get grouping stats
    abf.APs=cm.matrixfromDicts(abf.APs)
    abf.SAP=cm.matrixfromDicts(abf.SAP)
    print(" -- analyzed %d APs in %.02f ms"%(len(cm.dictFlat(abf.APs)),(time.clock()-timeStart)*1000))
    if saveToo:
        abf.saveThing(abf.APs,"APs")
        abf.saveThing(abf.SAP,"SAP")