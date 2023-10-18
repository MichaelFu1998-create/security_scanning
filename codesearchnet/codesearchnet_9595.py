def extract_subset(self, input_data_tiles=None, out_tile=None):
        """
        Extract subset from multiple tiles.

        input_data_tiles : list of (``Tile``, process data) tuples
        out_tile : ``Tile``

        Returns
        -------
        NumPy array or list of features.
        """
        if self.METADATA["data_type"] == "raster":
            mosaic = create_mosaic(input_data_tiles)
            return extract_from_array(
                in_raster=prepare_array(
                    mosaic.data,
                    nodata=self.nodata,
                    dtype=self.output_params["dtype"]
                ),
                in_affine=mosaic.affine,
                out_tile=out_tile
            )
        elif self.METADATA["data_type"] == "vector":
            return [
                feature for feature in list(
                    chain.from_iterable([features for _, features in input_data_tiles])
                )
                if shape(feature["geometry"]).intersects(out_tile.bbox)
            ]