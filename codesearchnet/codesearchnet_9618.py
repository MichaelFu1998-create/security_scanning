def profile(self, tile=None):
        """
        Create a metadata dictionary for rasterio.

        Parameters
        ----------
        tile : ``BufferedTile``

        Returns
        -------
        metadata : dictionary
            output profile dictionary used for rasterio.
        """
        dst_metadata = PNG_DEFAULT_PROFILE
        dst_metadata.pop("transform", None)
        if tile is not None:
            dst_metadata.update(
                width=tile.width, height=tile.height, affine=tile.affine,
                crs=tile.crs)
        try:
            dst_metadata.update(count=self.output_params["count"])
        except KeyError:
            pass
        return dst_metadata