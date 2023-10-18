def sweepYfiltered(self):
        """
        Get the filtered sweepY of the current sweep.
        Only works if self.kernel has been generated.
        """
        assert self.kernel is not None
        return swhlab.common.convolve(self.sweepY,self.kernel)