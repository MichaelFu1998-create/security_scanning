def up(self,x,L_change = 12):
        """
        Upsample and filter the signal
        """
        y = L_change*ssd.upsample(x,L_change)
        y = signal.lfilter(self.b,[1],y)
        return y