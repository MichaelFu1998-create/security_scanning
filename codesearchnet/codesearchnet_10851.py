def up(self,x):
        """
        Upsample and filter the signal
        """
        y = self.M*ssd.upsample(x,self.M)
        y = signal.lfilter(self.b,self.a,y)
        return y