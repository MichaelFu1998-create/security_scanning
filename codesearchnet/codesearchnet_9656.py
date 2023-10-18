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
        return reproject_geometry(
            self.process.config.area_at_zoom(),
            src_crs=self.process.config.process_pyramid.crs,
            dst_crs=self.pyramid.crs if out_crs is None else out_crs
        )