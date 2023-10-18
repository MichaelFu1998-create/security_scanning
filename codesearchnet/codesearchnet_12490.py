def ndwi(self):
        """
        Calculates Normalized Difference Water Index using Coastal and NIR2 bands for WV02, WV03.
        For Landsat8 and sentinel2 calculated by using Green and NIR bands.

        Returns: numpy array of ndwi values
        """
        data = self._read(self[self._ndwi_bands,...]).astype(np.float32)
        return (data[1,:,:] - data[0,:,:]) / (data[0,:,:] + data[1,:,:])