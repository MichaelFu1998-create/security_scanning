def for_web(self, data):
        """
        Convert data to web output (raster only).

        Parameters
        ----------
        data : array

        Returns
        -------
        web data : array
        """
        return memory_file(
            prepare_array(
                data, masked=True, nodata=self.nodata, dtype=self.profile()["dtype"]
            ),
            self.profile()
        ), "image/tiff"