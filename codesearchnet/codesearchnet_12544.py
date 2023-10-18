def aoi(self, **kwargs):
        """ Subsets the Image by the given bounds

        Args:
            bbox (list): optional. A bounding box array [minx, miny, maxx, maxy]
            wkt (str): optional. A WKT geometry string
            geojson (str): optional. A GeoJSON geometry dictionary

        Returns:
            image: an image instance of the same type
        """
        g = self._parse_geoms(**kwargs)
        if g is None:
            return self
        else:
            return self[g]