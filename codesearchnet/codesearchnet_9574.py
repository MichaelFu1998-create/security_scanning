def is_valid_with_config(self, config):
        """
        Check if output format is valid with other process parameters.

        Parameters
        ----------
        config : dictionary
            output configuration parameters

        Returns
        -------
        is_valid : bool
        """
        validate_values(config, [("schema", dict), ("path", str)])
        validate_values(config["schema"], [("properties", dict), ("geometry", str)])
        if config["schema"]["geometry"] not in [
            "Geometry", "Point", "MultiPoint", "Line", "MultiLine",
            "Polygon", "MultiPolygon"
        ]:
            raise TypeError("invalid geometry type")
        return True