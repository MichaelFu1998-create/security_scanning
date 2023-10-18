def average(self,t1=0,t2=None,setsweep=False):
        """return the average of part of the current sweep."""
        if setsweep:
            self.setsweep(setsweep)
        if t2 is None or t2>self.sweepLength:
            t2=self.sweepLength
            self.log.debug("resetting t2 to [%f]",t2)
        t1=max(t1,0)
        if t1>t2:
            self.log.error("t1 cannot be larger than t2")
            return False
        I1,I2=int(t1*self.pointsPerSec),int(t2*self.pointsPerSec)
        if I1==I2:
            return np.nan
        return np.average(self.sweepY[I1:I2])