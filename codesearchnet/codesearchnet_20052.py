def phasicTonic(self,m1=None,m2=None,chunkMs=50,quietPercentile=10,
                    histResolution=.5,plotToo=False):
        """ 
        let's keep the chunkMs as high as we reasonably can. 50ms is good.
        Things get flakey at lower numbers like 10ms.
        
        IMPORTANT! for this to work, prevent 0s from averaging in, so keep
        bin sizes well above the data resolution.
        """
        # prepare sectioning values to be used later
        m1=0 if m1 is None else m1*self.pointsPerSec
        m2=len(abf.sweepY) if m2 is None else m2*self.pointsPerSec
        m1,m2=int(m1),int(m2)
        
        # prepare histogram values to be used later
        padding=200 # pA or mV of maximum expected deviation
        chunkPoints=int(chunkMs*self.pointsPerMs)
        histBins=int((padding*2)/histResolution)
        
        # center the data at 0 using peak histogram, not the mean
        Y=self.sweepY[m1:m2]
        hist,bins=np.histogram(Y,bins=2*padding)
        Yoffset=bins[np.where(hist==max(hist))[0][0]]
        Y=Y-Yoffset # we don't have to, but PDF math is easier
        
        # calculate all histogram
        nChunks=int(len(Y)/chunkPoints)
        hist,bins=np.histogram(Y,bins=histBins,range=(-padding,padding))
        hist=hist/len(Y) # count as a fraction of total
        Xs=bins[1:]

        # get baseline data from chunks with smallest variance
        chunks=np.reshape(Y[:nChunks*chunkPoints],(nChunks,chunkPoints))
        variances=np.var(chunks,axis=1)
        percentiles=np.empty(len(variances))
        for i,variance in enumerate(variances):
            percentiles[i]=sorted(variances).index(variance)/len(variances)*100
        blData=chunks[np.where(percentiles<=quietPercentile)[0]].flatten()
        
        # generate the standard curve and pull it to the histogram height
        sigma=np.sqrt(np.var(blData))
        center=np.average(blData)+histResolution/2
        blCurve=mlab.normpdf(Xs,center,sigma)
        blCurve=blCurve*max(hist)/max(blCurve)
                
        # determine the phasic current by subtracting-out the baseline
        #diff=hist-blCurve
        diff=hist
        
        IGNORE_DISTANCE=5 # KEEP THIS FIXED, NOT A FUNCTION OF VARIANCE
        ignrCenter=len(Xs)/2
        ignrPad=IGNORE_DISTANCE/histResolution
        ignr1,ignt2=int(ignrCenter-ignrPad),int(ignrCenter+ignrPad)
        diff[ignr1:ignt2]=0
               
        # optionally graph all this
        if plotToo:
            plt.figure(figsize=(15,5))
            plt.plot(Y)
            plt.figure(figsize=(7,7))
            ax1=plt.subplot(211)
            plt.title(abf.ID+" phasic analysis")
            plt.ylabel("fraction")
            plt.plot(Xs,hist,'-',alpha=.8,color='b',lw=3)
            plt.plot(Xs,blCurve,lw=3,alpha=.5,color='r')
            plt.margins(0,.1)
            plt.subplot(212,sharex=ax1)
            plt.title("baseline subtracted")
            plt.ylabel("fraction")
            plt.xlabel("data points (%s)"%abf.units)
            plt.plot(Xs,diff,'-',alpha=.8,color='b',lw=3)
            plt.axhline(0,lw=3,alpha=.5,color='r')
            plt.axvline(0,lw=3,alpha=.5,color='k')
            plt.margins(0,.1)
            plt.axis([-50,50,None,None])
            plt.tight_layout()
            plt.show()
            
            print(np.sum(np.split(diff,2),1))
            
        return diff/len(Y)*abf.pointsPerSec