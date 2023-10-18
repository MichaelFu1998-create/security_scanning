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
        dst_metadata = dict(self._profile)
        if tile is not None:
            dst_metadata.update(
                width=tile.width,
                height=tile.height,
                affine=tile.affine, driver="PNG",
                crs=tile.crs
            )
        return dst_metadata