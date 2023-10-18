def get_bySweep(self,feature="freqs"):
        """
        returns AP info by sweep arranged as a list (by sweep).

        feature:
            * "freqs" - list of instantaneous frequencies by sweep.
            * "firsts" - list of first instantaneous frequency by sweep.
            * "times" - list of times of each AP in the sweep.
            * "count" - numer of APs per sweep.
            * "average" - average instanteous frequency per sweep.
            * "median" - median instanteous frequency per sweep.
        """
        self.ensureDetection()
        bySweepTimes=[[]]*self.abf.sweeps

        # determine AP spike times by sweep
        for sweep in range(self.abf.sweeps):
            sweepTimes=[]
            for ap in self.APs:
                if ap["sweep"]==sweep:
                    sweepTimes.append(ap["Tsweep"])
            bySweepTimes[sweep]=sweepTimes

        # determine instantaneous frequencies by sweep
        bySweepFreqs=[[]]*self.abf.sweeps
        for i,times in enumerate(bySweepTimes):
            if len(times)<2:
                continue
            diffs=np.array(times[1:])-np.array(times[:-1])
            bySweepFreqs[i]=np.array(1/diffs).tolist()

        # give the user what they want
        if feature == "freqs":
            return bySweepFreqs

        elif feature == "firsts":
            result=np.zeros(self.abf.sweeps) # initialize to this
            for i,freqs in enumerate(bySweepFreqs):
                if len(freqs):
                    result[i]=freqs[0]
            return result

        elif feature == "times":
            return bySweepTimes

        elif feature == "count":
            result=np.zeros(self.abf.sweeps) # initialize to this
            for i,times in enumerate(bySweepTimes):
                result[i]=len(bySweepTimes[i])
            return result

        elif feature == "average":
            result=np.zeros(self.abf.sweeps) # initialize to this
            for i,freqs in enumerate(bySweepFreqs):
                if len(freqs):
                    result[i]=np.nanmean(freqs)
            return result

        elif feature == "median":
            result=np.zeros(self.abf.sweeps) # initialize to this
            for i,freqs in enumerate(bySweepFreqs):
                if len(freqs):
                    result[i]=np.nanmedian(freqs)
            return result

        else:
            self.log.error("get_bySweep() can't handle [%s]",feature)
            return None