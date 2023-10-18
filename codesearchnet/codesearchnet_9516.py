def read(self, output_tile, **kwargs):
        """
        Read existing process output.

        Parameters
        ----------
        output_tile : ``BufferedTile``
            must be member of output ``TilePyramid``

        Returns
        -------
        process output : ``BufferedTile`` with appended data
        """
        try:
            return ma.masked_values(
                read_raster_no_crs(
                    self.get_path(output_tile), indexes=(4 if self.old_band_num else 2)
                ),
                0
            )
        except FileNotFoundError:
            return self.empty(output_tile)