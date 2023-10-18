def for_web(self, data):
        """
        Convert data to web output.

        Parameters
        ----------
        data : array

        Returns
        -------
        web data : array
        """
        rgba = self._prepare_array_for_png(data)
        data = ma.masked_where(rgba == self.nodata, rgba)
        return memory_file(data, self.profile()), 'image/png'