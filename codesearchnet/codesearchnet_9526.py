def execute(self, process_tile, raise_nodata=False):
        """
        Run the Mapchete process.

        Execute, write and return data.

        Parameters
        ----------
        process_tile : Tile or tile index tuple
            Member of the process tile pyramid (not necessarily the output
            pyramid, if output has a different metatiling setting)

        Returns
        -------
        data : NumPy array or features
            process output
        """
        if self.config.mode not in ["memory", "continue", "overwrite"]:
            raise ValueError("process mode must be memory, continue or overwrite")
        if isinstance(process_tile, tuple):
            process_tile = self.config.process_pyramid.tile(*process_tile)
        elif isinstance(process_tile, BufferedTile):
            pass
        else:
            raise TypeError("process_tile must be tuple or BufferedTile")

        if process_tile.zoom not in self.config.zoom_levels:
            return self.config.output.empty(process_tile)

        return self._execute(process_tile, raise_nodata=raise_nodata)