def read(self, indexes=None, **kwargs):
        """
        Read reprojected & resampled input data.

        Parameters
        ----------
        indexes : integer or list
            band number or list of band numbers

        Returns
        -------
        data : array
        """
        band_indexes = self._get_band_indexes(indexes)
        arr = self.process.get_raw_output(self.tile)
        if len(band_indexes) == 1:
            return arr[band_indexes[0] - 1]
        else:
            return ma.concatenate([ma.expand_dims(arr[i - 1], 0) for i in band_indexes])