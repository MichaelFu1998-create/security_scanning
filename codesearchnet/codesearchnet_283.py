def draw_points_heatmap_array(self, image_shape, alpha=1.0,
                                  size=1, raise_if_out_of_image=False):
        """
        Draw the points of the line string as a heatmap array.

        Parameters
        ----------
        image_shape : tuple of int
            The shape of the image onto which to draw the point mask.

        alpha : float, optional
            Opacity of the line string points. Higher values denote a more
            visible points.

        size : int, optional
            Size of the points in pixels.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if the line string is fully
            outside of the image. If set to False, no error will be raised and
            only the parts inside the image will be drawn.

        Returns
        -------
        ndarray
            Float array of shape `image_shape` (no channel axis) with drawn
            line string points. All values are in the interval ``[0.0, 1.0]``.

        """
        assert len(image_shape) == 2 or (
            len(image_shape) == 3 and image_shape[-1] == 1), (
            "Expected (H,W) or (H,W,1) as image_shape, got %s." % (
                image_shape,))

        arr = self.draw_points_on_image(
            np.zeros(image_shape, dtype=np.uint8),
            color=255, alpha=alpha, size=size,
            raise_if_out_of_image=raise_if_out_of_image
        )
        return arr.astype(np.float32) / 255.0