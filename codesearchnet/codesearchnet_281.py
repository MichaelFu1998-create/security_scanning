def draw_mask(self, image_shape, size_lines=1, size_points=0,
                  raise_if_out_of_image=False):
        """
        Draw this line segment as a binary image mask.

        Parameters
        ----------
        image_shape : tuple of int
            The shape of the image onto which to draw the line mask.

        size_lines : int, optional
            Thickness of the line segments.

        size_points : int, optional
            Size of the points in pixels.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if the line string is fully
            outside of the image. If set to False, no error will be raised and
            only the parts inside the image will be drawn.

        Returns
        -------
        ndarray
            Boolean line mask of shape `image_shape` (no channel axis).

        """
        heatmap = self.draw_heatmap_array(
            image_shape,
            alpha_lines=1.0, alpha_points=1.0,
            size_lines=size_lines, size_points=size_points,
            antialiased=False,
            raise_if_out_of_image=raise_if_out_of_image)
        return heatmap > 0.5