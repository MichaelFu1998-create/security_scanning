def ndvi(self, **kwargs):
        """
        Calculates Normalized Difference Vegetation Index using NIR and Red of an image.

        Returns: numpy array with ndvi values
        """
        data = self._read(self[self._ndvi_bands,...]).astype(np.float32)
        return (data[0,:,:] - data[1,:,:]) / (data[0,:,:] + data[1,:,:])