def dn(self,x):
        """
        Downsample and filter the signal
        """
        y = signal.lfilter(self.b,self.a,x)
        y = ssd.downsample(y,self.M)
        return y