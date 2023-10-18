def periodogram(self):
        """An alias to :class:`~spectrum.periodogram.Periodogram`

        The parameters are extracted from the attributes. Relevant attributes
        ares :attr:`window`, attr:`sampling`, attr:`NFFT`, attr:`scale_by_freq`,
        :attr:`detrend`.

        .. plot::
            :width: 80%
            :include-source:

            from spectrum import datasets
            from spectrum import FourierSpectrum
            s = FourierSpectrum(datasets.data_cosine(), sampling=1024, NFFT=512)
            s.periodogram()
            s.plot()
        """
        from .periodogram import speriodogram
        psd = speriodogram(self.data, window=self.window, sampling=self.sampling,
                             NFFT=self.NFFT, scale_by_freq=self.scale_by_freq,
                             detrend=self.detrend)
        self.psd = psd