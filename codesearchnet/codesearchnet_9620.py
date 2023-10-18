def empty(self, process_tile):
        """
        Return empty data.

        Parameters
        ----------
        process_tile : ``BufferedTile``
            must be member of process ``TilePyramid``

        Returns
        -------
        empty data : array
            empty array with data type given in output parameters
        """
        bands = (
            self.output_params["bands"]
            if "bands" in self.output_params
            else PNG_DEFAULT_PROFILE["count"]
        )
        return ma.masked_array(
            data=ma.zeros((bands, ) + process_tile.shape),
            mask=ma.zeros((bands, ) + process_tile.shape),
            dtype=PNG_DEFAULT_PROFILE["dtype"]
        )