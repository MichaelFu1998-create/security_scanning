def geotiff(self, **kwargs):
        """ Creates a geotiff on the filesystem

        Args:
            path (str): optional, path to write the geotiff file to, default is ./output.tif
            proj (str): optional, EPSG string of projection to reproject to
            spec (str): optional, if set to 'rgb', write out color-balanced 8-bit RGB tif
            bands (list): optional, list of bands to export. If spec='rgb' will default to RGB bands,
                otherwise will export all bands

        Returns:
            str: path the geotiff was written to """

        if 'proj' not in kwargs:
            kwargs['proj'] = self.proj
        return to_geotiff(self, **kwargs)