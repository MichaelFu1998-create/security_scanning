def read(self, bands=None, **kwargs):
        """Reads data from a dask array and returns the computed ndarray matching the given bands

        Args:
            bands (list): band indices to read from the image. Returns bands in the order specified in the list of bands.

        Returns:
            ndarray: a numpy array of image data
        """
        arr = self
        if bands is not None:
            arr = self[bands, ...]
        return arr.compute(scheduler=threaded_get)