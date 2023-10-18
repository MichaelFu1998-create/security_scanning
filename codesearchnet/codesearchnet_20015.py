def phasicTonic(self,m1=None,m2=None,chunkMs=50,
                    quietPercentile=10,histResolution=1):
        """ 
        chunkMs should be ~50 ms or greater.
        bin sizes must be equal to or multiples of the data resolution.
        transients smaller than the expected RMS will be silenced.
        """
        # prepare sectioning values to be used later (marker positions)
        m1=0 if m1 is None else m1*self.pointsPerSec
        m2=len(abf.sweepY) if m2 is None else m2*self.pointsPerSec
        m1,m2=int(m1),int(m2)
        
        # prepare histogram values to be used later
        padding=200 # pA or mV of maximum expected deviation
        chunkPoints=int(chunkMs*self.pointsPerMs)
        histBins=int((padding*2)/histResolution)
        
        # center the data at 0 using peak histogram, not the mean
        #Y=self.sweepY[m1:m2]
        Y=self.sweepYfilteredHisto()[m1:m2]
        hist,bins=np.histogram(Y,bins=2*padding)
        #Yoffset=bins[np.where(hist==max(hist))[0][0]]
        #Y=Y-Yoffset # we don't have to, but PDF math is easier
        
        # create histogram for all data in the sweep
        nChunks=int(len(Y)/chunkPoints)
        hist,bins=np.histogram(Y,bins=histBins,range=(-padding,padding))

        # create histogram for just the sweeps with the lowest variance
        chunks=np.reshape(Y[:nChunks*chunkPoints],(nChunks,chunkPoints))
        #variances=np.var(chunks,axis=1)
        variances=np.ptp(chunks,axis=1)
        percentiles=np.empty(len(variances))
        for i,variance in enumerate(variances):
            percentiles[i]=sorted(variances).index(variance)/len(variances)*100
        blData=chunks[np.where(percentiles<=quietPercentile)[0]].flatten()
        blHist,blBins=np.histogram(blData,bins=histBins,range=(-padding,padding))
        blHist=blHist/max(blHist)*max(hist)
        
        # determine the phasic current by subtracting-out the baseline
        diff=hist-blHist
        return diff/abf.pointsPerSec