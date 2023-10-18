def get_times(self):
        """return an array of times (in sec) of all APs."""
        self.ensureDetection()
        times=[]
        for ap in self.APs:
            times.append(ap["T"])
        return np.array(sorted(times))