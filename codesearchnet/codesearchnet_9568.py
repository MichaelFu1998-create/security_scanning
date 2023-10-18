def read(self, indexes=None, **kwargs):
        """
        Read reprojected & resampled input data.

        Returns
        -------
        data : array
        """
        return read_raster_window(
            self.raster_file.path,
            self.tile,
            indexes=self._get_band_indexes(indexes),
            resampling=self.resampling,
            gdal_opts=self.gdal_opts
        )