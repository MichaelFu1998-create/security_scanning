def average_data(self,ranges=[[None,None]],percentile=None):
        """
        given a list of ranges, return single point averages for every sweep.
        Units are in seconds. Expects something like:
            ranges=[[1,2],[4,5],[7,7.5]]
        None values will be replaced with maximum/minimum bounds.
        For baseline subtraction, make a range baseline then sub it youtself.
            returns datas[iSweep][iRange][AVorSD]
        if a percentile is given, return that percentile rather than average.
            percentile=50 is the median, but requires sorting, and is slower.
        """
        ranges=copy.deepcopy(ranges) #TODO: make this cleaner. Why needed?
        # clean up ranges, make them indexes
        for i in range(len(ranges)):
            if ranges[i][0] is None:
                ranges[i][0] = 0
            else:
                ranges[i][0] = int(ranges[i][0]*self.rate)
            if ranges[i][1] is None:
                ranges[i][1] = -1
            else:
                ranges[i][1] = int(ranges[i][1]*self.rate)

        # do the math
        datas=np.empty((self.sweeps,len(ranges),2)) #[sweep][range]=[Av,Er]
        for iSweep in range(self.sweeps):
            self.setSweep(iSweep)
            for iRange in range(len(ranges)):
                I1=ranges[iRange][0]
                I2=ranges[iRange][1]
                if percentile:
                    datas[iSweep][iRange][0]=np.percentile(self.dataY[I1:I2],percentile)
                else:
                    datas[iSweep][iRange][0]=np.average(self.dataY[I1:I2])
                datas[iSweep][iRange][1]=np.std(self.dataY[I1:I2])
        return datas