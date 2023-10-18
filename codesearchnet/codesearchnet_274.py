def project(self, from_shape, to_shape):
        """
        Project the line string onto a differently shaped image.

        E.g. if a point of the line string is on its original image at
        ``x=(10 of 100 pixels)`` and ``y=(20 of 100 pixels)`` and is projected
        onto a new image with size ``(width=200, height=200)``, its new
        position will be ``(x=20, y=40)``.

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
        out : imgaug.augmentables.lines.LineString
            Line string with new coordinates.

        """
        coords_proj = project_coords(self.coords, from_shape, to_shape)
        return self.copy(coords=coords_proj)