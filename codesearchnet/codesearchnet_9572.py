def read(self, output_tile, **kwargs):
        """
        Read existing process output.

        Parameters
        ----------
        output_tile : ``BufferedTile``
            must be member of output ``TilePyramid``

        Returns
        -------
        process output : list
        """
        path = self.get_path(output_tile)
        try:
            with fiona.open(path, "r") as src:
                return list(src)
        except DriverError as e:
            for i in ("does not exist in the file system", "No such file or directory"):
                if i in str(e):
                    return self.empty(output_tile)
            else:
                raise