def clip_out_of_image(self):
        """
        Clip off all parts from all polygons that are outside of the image.

        NOTE: The result can contain less polygons than the input did. That
        happens when a polygon is fully outside of the image plane.

        NOTE: The result can also contain *more* polygons than the input
        did. That happens when distinct parts of a polygon are only
        connected by areas that are outside of the image plane and hence will
        be clipped off, resulting in two or more unconnected polygon parts that
        are left in the image plane.

        Returns
        -------
        imgaug.PolygonsOnImage
            Polygons, clipped to fall within the image dimensions. Count of
            output polygons may differ from the input count.

        """
        polys_cut = [
            poly.clip_out_of_image(self.shape)
            for poly
            in self.polygons
            if poly.is_partly_within_image(self.shape)
        ]
        polys_cut_flat = [poly for poly_lst in polys_cut for poly in poly_lst]
        # TODO use deepcopy() here
        return PolygonsOnImage(polys_cut_flat, shape=self.shape)