def _df(self):
        """
        Degrees of freedom.
        """
        if not self._restricted:
            return self.nsamples
        return self.nsamples - self._X["tX"].shape[1]