def get_scale(self):
        """
        If exposure was not set in the __init__, get the exposure associated
        with this RawImage so that it may be used in other
        :class:`~peri.util.RawImage`. This is useful for transferring exposure
        parameters to a series of images.

        Returns
        -------
        exposure : tuple of floats
            The (emin, emax) which get mapped to (0, 1)
        """
        if self.exposure is not None:
            return self.exposure

        raw = initializers.load_tiff(self.filename)
        return raw.min(), raw.max()