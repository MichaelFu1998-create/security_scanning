def read(self, output_tile):
        """
        Read from written process output.

        Parameters
        ----------
        output_tile : BufferedTile or tile index tuple
            Member of the output tile pyramid (not necessarily the process
            pyramid, if output has a different metatiling setting)

        Returns
        -------
        data : NumPy array or features
            process output
        """
        if self.config.mode not in ["readonly", "continue", "overwrite"]:
            raise ValueError("process mode must be readonly, continue or overwrite")
        if isinstance(output_tile, tuple):
            output_tile = self.config.output_pyramid.tile(*output_tile)
        elif isinstance(output_tile, BufferedTile):
            pass
        else:
            raise TypeError("output_tile must be tuple or BufferedTile")

        return self.config.output.read(output_tile)