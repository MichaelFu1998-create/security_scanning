def open(self, input_id, **kwargs):
        """
        Open input data.

        Parameters
        ----------
        input_id : string
            input identifier from configuration file or file path
        kwargs : driver specific parameters (e.g. resampling)

        Returns
        -------
        tiled input data : InputTile
            reprojected input data within tile
        """
        if not isinstance(input_id, str):
            return input_id.open(self.tile, **kwargs)
        if input_id not in self.params["input"]:
            raise ValueError("%s not found in config as input file" % input_id)
        return self.params["input"][input_id].open(self.tile, **kwargs)