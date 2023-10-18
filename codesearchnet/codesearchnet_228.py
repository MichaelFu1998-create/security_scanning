def remove_out_of_image(self, fully=True, partly=False):
        """
        Remove all polygons that are fully or partially outside of the image.

        Parameters
        ----------
        fully : bool, optional
            Whether to remove polygons that are fully outside of the image.

        partly : bool, optional
            Whether to remove polygons that are partially outside of the image.

        Returns
        -------
        imgaug.PolygonsOnImage
            Reduced set of polygons, with those that were fully/partially
            outside of the image removed.

        """
        polys_clean = [
            poly for poly in self.polygons
            if not poly.is_out_of_image(self.shape, fully=fully, partly=partly)
        ]
        # TODO use deepcopy() here
        return PolygonsOnImage(polys_clean, shape=self.shape)