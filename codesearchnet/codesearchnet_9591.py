def get_path(self, tile):
        """
        Determine target file path.

        Parameters
        ----------
        tile : ``BufferedTile``
            must be member of output ``TilePyramid``

        Returns
        -------
        path : string
        """
        return os.path.join(*[
            self.path,
            str(tile.zoom),
            str(tile.row),
            str(tile.col) + self.file_extension
        ])