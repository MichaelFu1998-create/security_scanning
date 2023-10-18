def compute_response(self, **kargs):
        """Compute the window data frequency response

        :param norm: True by default. normalised the frequency data.
        :param int NFFT: total length of the final data sets( 2048 by default. 
            if less than data length, then NFFT is set to the data length*2).

        The response is stored in :attr:`response`.

        .. note:: Units are dB (20 log10) since we plot the frequency response)

        """
        from numpy.fft import fft, fftshift

        norm = kargs.get('norm', self.norm)

        # do some padding. Default is max(2048, data.len*2)
        NFFT = kargs.get('NFFT', 2048)
        if NFFT < len(self.data):
            NFFT = self.data.size * 2

        # compute the fft modulus
        A = fft(self.data, NFFT)
        mag = abs(fftshift(A))

        # do we want to normalise the data
        if norm is True:
            mag = mag / max(mag)

        response = 20. * stools.log10(mag) # factor 20 we are looking at the response
                                    # not the powe
        #response = clip(response,mindB,100)
        self.__response = response