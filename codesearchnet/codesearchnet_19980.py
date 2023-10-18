def average_sweep(self,T1=0,T2=None,sweeps=None,stdErr=False):
        """
        given an array of sweeps, return X,Y,Err average.
        This returns *SWEEPS* of data, not just 1 data point.
        """
        T1=T1*self.rate
        if T2 is None:
            T2 = self.sweepSize-1
        else:
            T2 = T2*self.rate
        if sweeps is None:
            sweeps = range(self.sweeps)
        Ys=np.empty((len(sweeps),(T2-T1)))
        for i in range(len(sweeps)):
            self.setSweep(sweeps[i])
            Ys[i]=self.dataY[T1:T2]
        Av = np.average(Ys,0)
        Es = np.std(Ys,0)
        Xs = self.dataX[T1:T2]
        if stdErr: #otherwise return stdev
            Es = Es/np.sqrt(len(sweeps))
        return Xs,Av,Es