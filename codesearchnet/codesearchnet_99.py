def project(self, from_shape, to_shape):
        """
        Project the keypoint onto a new position on a new image.

        E.g. if the keypoint is on its original image at x=(10 of 100 pixels)
        and y=(20 of 100 pixels) and is projected onto a new image with
        size (width=200, height=200), its new position will be (20, 40).

        This is intended for cases where the original image is resized.
        It cannot be used for more complex changes (e.g. padding, cropping).

        Parameters
        ----------
        from_shape : tuple of int
            Shape of the original image. (Before resize.)

        to_shape : tuple of int
            Shape of the new image. (After resize.)

        Returns
        -------
        imgaug.Keypoint
            Keypoint object with new coordinates.

        """
        xy_proj = project_coords([(self.x, self.y)], from_shape, to_shape)
        return self.deepcopy(x=xy_proj[0][0], y=xy_proj[0][1])