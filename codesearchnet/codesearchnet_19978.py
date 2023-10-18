def clampValues(self,timePoint=0):
        """
        return an array of command values at a time point (in sec).
        Useful for things like generating I/V curves.
        """
        Cs=np.zeros(self.sweeps)
        for i in range(self.sweeps):
            self.setSweep(i) #TODO: protocol only = True
            for j in range(len(self.protoSeqX)):
                if self.protoSeqX[j]<=timePoint*self.rate:
                    Cs[i]=self.protoSeqY[j]
        return Cs