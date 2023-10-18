def bbox(self, out_crs=None):
        """
        Return data bounding box.

        Parameters
        ----------
        out_crs : ``rasterio.crs.CRS``
            rasterio CRS object (default: CRS of process pyramid)

        Returns
        -------
        bounding box : geometry
            Shapely geometry object
        """
        out_crs = self.pyramid.crs if out_crs is None else out_crs
        with fiona.open(self.path) as inp:
            inp_crs = CRS(inp.crs)
            bbox = box(*inp.bounds)
        # TODO find a way to get a good segmentize value in bbox source CRS
        return reproject_geometry(bbox, src_crs=inp_crs, dst_crs=out_crs)