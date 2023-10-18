def project(self, from_shape, to_shape):
        """
        Project the bounding box onto a differently shaped image.

        E.g. if the bounding box is on its original image at
        x1=(10 of 100 pixels) and y1=(20 of 100 pixels) and is projected onto
        a new image with size (width=200, height=200), its new position will
        be (x1=20, y1=40). (Analogous for x2/y2.)

        This is intended for cases where the original image is resized.
        It cannot be used for more complex changes (e.g. padding, cropping).

        Parameters
        ----------
        from_shape : tuple of int or ndarray
            Shape of the original image. (Before resize.)

        to_shape : tuple of int or ndarray
            Shape of the new image. (After resize.)

        Returns
        -------
        out : imgaug.BoundingBox
            BoundingBox object with new coordinates.

        """
        coords_proj = project_coords([(self.x1, self.y1), (self.x2, self.y2)],
                                     from_shape, to_shape)
        return self.copy(
            x1=coords_proj[0][0],
            y1=coords_proj[0][1],
            x2=coords_proj[1][0],
            y2=coords_proj[1][1],
            label=self.label)