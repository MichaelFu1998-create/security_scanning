def sim(self, src, tar, *args, **kwargs):
        """Return similarity.

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
        float
            Similarity

        """
        return 1.0 - self.dist(src, tar, *args, **kwargs)