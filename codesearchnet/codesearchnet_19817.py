def phasicNet(self,biggestEvent=50,m1=.5,m2=None):
        """
        Calculates the net difference between positive/negative phasic events
        Returns return the phasic difference value of the current sweep.

        Arguments:
            biggestEvent (int): the size of the largest event anticipated
            m1 (int, optional): the time (sec) to start analyzing
            m2 (int, optional): the time (sec) to end analyzing

        Example:
            abf=swhlab.ABF(abfFile)
            abf.kernel=abf.kernel_gaussian(sizeMS=500) # kernel for smart baseline
            diff=[]
            for sweep in abf.setsweeps():
                print("Sweep",sweep)
                diff.append(analyzeSweep(abf,plot=True,label="sweep %d"%sweep))
            print(diff)
        """

        # determine marks (between which we will analyze)
        m1=0 if m1 is None else self.pointsPerSec*m1
        m2=-1 if m2 is None else self.pointsPerSec*m2

        # acquire the baseline-subtracted sweep
        Y=self.sweepYsmartbase()[int(m1):int(m2)]

        # create the histogram
        nBins=1000
        hist,bins=np.histogram(Y,bins=nBins,range=[-biggestEvent,biggestEvent],density=True)
        histSmooth=swhlab.common.lowpass(hist)

        # normalize height to 1
        #TODO: should it be normalized first or not?
        #YES if reporting the ratio of the up/down area, NO if reporting the up-down difference
        #hist,histSmooth=hist/max(histSmooth),histSmooth/max(histSmooth)

        # center the peak at 0 pA
        peakI=np.where(histSmooth==max(histSmooth))[0][0]
        hist=np.roll(hist,int(nBins/2-peakI))
        histSmooth=np.roll(histSmooth,int(nBins/2-peakI))

        # calculate our mirrored difference
        downward,upward=np.split(histSmooth,2)
        downward=downward[::-1]
        diff=np.sum(upward-downward)

        # convert our "pA/time" to "pA/sec"
        diff=diff/(len(Y)/self.pointsPerSec)

        return diff