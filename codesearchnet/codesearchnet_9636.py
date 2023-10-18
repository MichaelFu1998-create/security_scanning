def read(self, validity_check=True, **kwargs):
        """
        Read reprojected & resampled input data.

        Parameters
        ----------
        validity_check : bool
            also run checks if reprojected geometry is valid, otherwise throw
            RuntimeError (default: True)

        Returns
        -------
        data : list
        """
        return [] if self.is_empty() else self._read_from_cache(validity_check)