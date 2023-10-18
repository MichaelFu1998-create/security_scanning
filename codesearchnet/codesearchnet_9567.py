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
        with rasterio.open(self.path) as inp:
            inp_crs = inp.crs
            out_bbox = bbox = box(*inp.bounds)
        # If soucre and target CRSes differ, segmentize and reproject
        if inp_crs != out_crs:
            # estimate segmentize value (raster pixel size * tile size)
            # and get reprojected bounding box
            return reproject_geometry(
                segmentize_geometry(
                    bbox, inp.transform[0] * self.pyramid.tile_size
                ),
                src_crs=inp_crs, dst_crs=out_crs
            )
        else:
            return out_bbox