def filter(self,x):
        """
        Filter the signal
        """
        y = signal.lfilter(self.b,[1],x)
        return y