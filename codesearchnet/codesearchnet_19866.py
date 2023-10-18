def analyzeAP(Y,dY,I,rate,verbose=False):
    """
    given a sweep and a time point, return the AP array for that AP.
    APs will be centered in time by their maximum upslope.
    """
    Ims = int(rate/1000) #Is per MS
    IsToLook=5*Ims #TODO: clarify this, ms until downslope is over
    upslope=np.max(dY[I:I+IsToLook]) #maximum rise velocity
    upslopeI=np.where(dY[I:I+IsToLook]==upslope)[0][0]+I
    I=upslopeI #center sweep at the upslope
    downslope=np.min(dY[I:I+IsToLook]) #maximum fall velocity
    downslopeI=np.where(dY[I:I+IsToLook]==downslope)[0][0]+I
    peak=np.max(Y[I:I+IsToLook]) #find peak value (mV)
    peakI=np.where(Y[I:I+IsToLook]==peak)[0][0]+I #find peak I
    thresholdI=I-np.where(dY[I:I+IsToLook:--1]<10)[0] #detect <10V/S
    if not len(thresholdI):
        return False
    thresholdI=thresholdI[0]
    threshold=Y[thresholdI] # mV where >10mV/S
    height=peak-threshold # height (mV) from threshold to peak
    halfwidthPoint=np.average((threshold,peak))
    halfwidth=np.where(Y[I-IsToLook:I+IsToLook]>halfwidthPoint)[0]
    if not len(halfwidth):
        return False #doesn't look like a real AP
    halfwidthI1=halfwidth[0]+I-IsToLook
    halfwidthI2=halfwidth[-1]+I-IsToLook
    if Y[halfwidthI1-1]>halfwidthPoint or Y[halfwidthI2+1]>halfwidthPoint:
        return False #doesn't look like a real AP
    halfwidth=len(halfwidth)/rate*1000 #now in MS
    riseTime=(peakI-thresholdI)*1000/rate # time (ms) from threshold to peak

    IsToLook=100*Ims #TODO: max prediction until AHP reaches nadir
    AHPchunk=np.diff(Y[downslopeI:downslopeI+IsToLook]) #first inflection
    AHPI=np.where(AHPchunk>0)[0]
    if len(AHPI)==0:
        AHPI=np.nan
    else:
        AHPI=AHPI[0]+downslopeI
        AHPchunk=Y[AHPI:AHPI+IsToLook]
        if max(AHPchunk)>threshold: #if another AP is coming, cut it out
            AHPchunk=AHPchunk[:np.where(AHPchunk>threshold)[0][0]]
        if len(AHPchunk):
            AHP=np.nanmin(AHPchunk)
            AHPI=np.where(AHPchunk==AHP)[0][0]+AHPI
            AHPheight=threshold-AHP # AHP magnitude from threshold (mV)
            IsToLook=500*Ims #TODO: max prediction until AHP reaches threshold
            AHPreturn=np.average((AHP,threshold)) #half of threshold
            AHPreturnI=np.where(Y[AHPI:AHPI+IsToLook]>AHPreturn)[0]
            if len(AHPreturnI): #not having a clean decay won't cause AP to crash
                AHPreturnI=AHPreturnI[0]+AHPI
                AHPrisetime=(AHPreturnI-AHPI)*2/rate*1000 #predicted return time (ms)
                AHPupslope=AHPheight/AHPrisetime #mV/ms = V/S
                AHPreturnFullI=(AHPreturnI-AHPI)*2+AHPI
            else: #make them nan so you can do averages later
                AHPreturnI,AHPrisetime,AHPupslope=np.nan,np.nan,np.nan
                downslope=np.nan

    #fasttime (10V/S to 10V/S) #TODO:
    #dpp (deriv peak to peak) #TODO:

    sweepI,sweepT=I,I/rate # clean up variable names
    del IsToLook,I, Y, dY, Ims, AHPchunk, verbose #delete what we don't need
    return locals()