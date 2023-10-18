def up(self,x,L_change = 12):
        """
        Upsample and filter the signal
        """
        y = L_change*ssd.upsample(x,L_change)
        y = signal.sosfilt(self.sos,y)
        return y