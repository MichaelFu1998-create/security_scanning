def read(self, validity_check=True, no_neighbors=False, **kwargs):
        """
        Read data from process output.

        Parameters
        ----------
        validity_check : bool
            run geometry validity check (default: True)
        no_neighbors : bool
            don't include neighbor tiles if there is a pixelbuffer (default:
            False)

        Returns
        -------
        features : list
            GeoJSON-like list of features
        """
        if no_neighbors:
            raise NotImplementedError()
        return self._from_cache(validity_check=validity_check)