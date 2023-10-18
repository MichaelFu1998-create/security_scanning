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
        dst_metadata = GTIFF_DEFAULT_PROFILE
        dst_metadata.pop("transform", None)
        dst_metadata.update(
            count=self.output_params["bands"],
            dtype=self.output_params["dtype"],
            driver="GTiff"
        )
        if tile is not None:
            dst_metadata.update(
                crs=tile.crs, width=tile.width, height=tile.height,
                affine=tile.affine)
        else:
            for k in ["crs", "width", "height", "affine"]:
                dst_metadata.pop(k, None)
        if "nodata" in self.output_params:
            dst_metadata.update(nodata=self.output_params["nodata"])
        try:
            if "compression" in self.output_params:
                warnings.warn(
                    DeprecationWarning("use 'compress' instead of 'compression'")
                )
                dst_metadata.update(compress=self.output_params["compression"])
            else:
                dst_metadata.update(compress=self.output_params["compress"])
            dst_metadata.update(predictor=self.output_params["predictor"])
        except KeyError:
            pass
        return dst_metadata