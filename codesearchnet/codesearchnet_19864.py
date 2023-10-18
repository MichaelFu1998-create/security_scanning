def analyzeAPgroup(abf=exampleABF,T1=None,T2=None,plotToo=False):
    """
    On the current (setSweep()) sweep, calculate things like accomodation.
    Only call directly just for demonstrating how it works by making a graph.
    Or call this if you want really custom T1 and T2 (multiple per sweep)
      This is called by default with default T1 and T2.
      Manually call it again for custom.
    """
    if T1 is None or T2 is None:
        if len(abf.protoSeqX)>2:
            T1=abf.protoSeqX[1]/abf.rate
            T2=abf.protoSeqX[2]/abf.rate
        else:
            T1=0
            T2=abf.sweepLength
    s={} #sweep dictionary to contain our stas
    s["sweep"]=abf.currentSweep
    s["commandI"]=abf.protoSeqY[1]

    APs=[]

    for key in ['freqAvg','freqBin']:
        s[key]=0

    for AP in abf.APs[abf.currentSweep]:
        if T1<AP["sweepT"]<T2:
            APs.append(AP)
    s["nAPs"]=len(APs) #number of APs in the bin period (T1-T2)
    apTimes=cm.dictVals(APs,'sweepT')
    if len(APs)>1: #some measurements require multiple APs, like accomodation
        s["centerBinTime"]=np.average(apTimes)-T1 #average time of APs in the bin
        s["centerBinFrac"]=s["centerBinTime"]/(T2-T1)*100 #fractional average of APs in bin (steady = .5)
        s["centerTime"]=np.average(apTimes)-APs[0]["sweepT"] #time of average AP WRT first AP (not bin)
        s["centerFrac"]=s["centerTime"]/(APs[-1]["sweepT"]-APs[0]["sweepT"])*100 #WRT first/last AP
        s["msToFirst"]=(APs[0]["sweepT"]-T1)*1000 #ms to first AP (from T1)
        s["freqFirst1"]=APs[1]['freq'] #inst frequency of first AP
        s["freqFirst5"]=cm.dictAvg(APs[1:6],'freq')[0] #inst frequency of first AP
        s["freqLast"]=APs[-1]['freq'] #inst frequency of last AP
        s["freqAvg"]=cm.dictAvg(APs,'freq')[0] #average inst frequency of all aps
        s["freqBin"]=len(APs)/(T2-T1) #frequency of APs in the bin (T1-T2)
        s["freqSteady25"]=cm.dictAvg(APs[-int(len(APs)*.25):],'freq')[0] # average freq of the last 25% of APs
        s["accom1Avg"]=s["freqFirst1"]/s["freqAvg"] #accomodation (first II / average)
        s["accom1Steady25"]=s["freqFirst1"]/s["freqSteady25"] #accomodation (first II / steady state)
        s["accom5Avg"]=s["freqFirst5"]/s["freqAvg"] #accomodation from average 5 first
        s["accom5Steady25"]=s["freqFirst5"]/s["freqSteady25"] #accomodation from average 5 first
        s["freqCV"]=cm.dictAvg(APs,'freq')[1]/cm.dictAvg(APs,'freq')[0] #coefficient of variation (Hz)
        s["T1"]=T1
        s["T2"]=T2
    abf.SAP[abf.currentSweep]=s