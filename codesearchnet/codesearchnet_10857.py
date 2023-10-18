def filter(self,x):
        """
        Filter the signal using second-order sections
        """
        y = signal.sosfilt(self.sos,x)
        return y