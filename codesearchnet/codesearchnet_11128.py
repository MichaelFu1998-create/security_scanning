def dist_abs(self, src, tar, *args, **kwargs):
        """Return absolute distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        int
            Absolute distance

        """
        return self.dist(src, tar, *args, **kwargs)