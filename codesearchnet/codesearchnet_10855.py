def dn(self,x,M_change = 12):
        """
        Downsample and filter the signal
        """
        y = signal.lfilter(self.b,[1],x)
        y = ssd.downsample(y,M_change)
        return y