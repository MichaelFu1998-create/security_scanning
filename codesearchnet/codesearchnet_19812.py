def epochTimes(self,nEpoch=2):
        """
        alternative to the existing abf protocol stuff
        return the start/stop time of an epoch.
        Epoch start at zero.
        A=0, B=1, C=2, D=3, ...
        """
        times=[]
        durations=[]
        for epoch in self.header['dictEpochInfoPerDAC'][self.channel].values():
            print(epoch['lEpochInitDuration']/self.pointsPerSec)
            times.append(sum(durations))
            durations.append(epoch['lEpochInitDuration']/self.pointsPerSec)
        times.append(sum(durations))
        times=np.array(times)+self.offsetX/self.pointsPerSec # WHY?!?
        if nEpoch:
            return times[nEpoch],times[nEpoch+1]
        else:
            return times