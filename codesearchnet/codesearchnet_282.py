def draw_lines_heatmap_array(self, image_shape, alpha=1.0,
                                 size=1, antialiased=True,
                                 raise_if_out_of_image=False):
        """
        Draw the line segments of the line string as a heatmap array.

        Parameters
        ----------
        image_shape : tuple of int
            The shape of the image onto which to draw the line mask.

        alpha : float, optional
            Opacity of the line string. Higher values denote a more visible
            line string.

        size : int, optional
            Thickness of the line segments.

        antialiased : bool, optional
            Whether to draw the line with anti-aliasing activated.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if the line string is fully
            outside of the image. If set to False, no error will be raised and
            only the parts inside the image will be drawn.

        Returns
        -------
        ndarray
            Float array of shape `image_shape` (no channel axis) with drawn
            line string. All values are in the interval ``[0.0, 1.0]``.

        """
        assert len(image_shape) == 2 or (
            len(image_shape) == 3 and image_shape[-1] == 1), (
            "Expected (H,W) or (H,W,1) as image_shape, got %s." % (
                image_shape,))

        arr = self.draw_lines_on_image(
            np.zeros(image_shape, dtype=np.uint8),
            color=255, alpha=alpha, size=size,
            antialiased=antialiased,
            raise_if_out_of_image=raise_if_out_of_image
        )
        return arr.astype(np.float32) / 255.0