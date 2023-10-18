def get_scale_from_raw(raw, scaled):
        """
        When given a raw image and the scaled version of the same image, it
        extracts the ``exposure`` parameters associated with those images.
        This is useful when

        Parameters
        ----------
        raw : array_like
            The image loaded fresh from a file

        scaled : array_like
            Image scaled using :func:`peri.initializers.normalize`

        Returns
        -------
        exposure : tuple of numbers
            Returns the exposure parameters (emin, emax) which get mapped to
            (0, 1) in the scaled image. Can be passed to
            :func:`~peri.util.RawImage.__init__`
        """
        t0, t1 = scaled.min(), scaled.max()
        r0, r1 = float(raw.min()), float(raw.max())

        rmin = (t1*r0 - t0*r1) / (t1 - t0)
        rmax = (r1 - r0) / (t1 - t0) + rmin
        return (rmin, rmax)