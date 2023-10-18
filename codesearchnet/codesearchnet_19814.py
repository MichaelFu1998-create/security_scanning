def averageSweep(self,sweepFirst=0,sweepLast=None):
        """
        Return a sweep which is the average of multiple sweeps.
        For now, standard deviation is lost.
        """
        if sweepLast is None:
            sweepLast=self.sweeps-1
        nSweeps=sweepLast-sweepFirst+1
        runningSum=np.zeros(len(self.sweepY))
        self.log.debug("averaging sweep %d to %d",sweepFirst,sweepLast)
        for sweep in np.arange(nSweeps)+sweepFirst:
            self.setsweep(sweep)
            runningSum+=self.sweepY.flatten()
        average=runningSum/nSweeps
        #TODO: standard deviation?
        return average