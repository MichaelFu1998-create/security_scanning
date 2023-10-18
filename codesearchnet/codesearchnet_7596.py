def power(self):
        r"""Return the power contained in the PSD

        if scale_by_freq is False, the power is:

        .. math:: P = N \sum_{k=1}^{N} P_{xx}(k)

        else, it is

        .. math:: P =  \sum_{k=1}^{N} P_{xx}(k) \frac{df}{2\pi}

        .. todo:: check these equations


        """
        if self.scale_by_freq == False:
            return sum(self.psd) * len(self.psd)
        else:
            return sum(self.psd) * self.df/(2.*numpy.pi)