def draw_heatmap_array(self, image_shape, alpha_lines=1.0, alpha_points=1.0,
                           size_lines=1, size_points=0, antialiased=True,
                           raise_if_out_of_image=False):
        """
        Draw the line segments and points of the line string as a heatmap array.

        Parameters
        ----------
        image_shape : tuple of int
            The shape of the image onto which to draw the line mask.

        alpha_lines : float, optional
            Opacity of the line string. Higher values denote a more visible
            line string.

        alpha_points : float, optional
            Opacity of the line string points. Higher values denote a more
            visible points.

        size_lines : int, optional
            Thickness of the line segments.

        size_points : int, optional
            Size of the points in pixels.

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
            line segments and points. All values are in the
            interval ``[0.0, 1.0]``.

        """
        heatmap_lines = self.draw_lines_heatmap_array(
            image_shape,
            alpha=alpha_lines,
            size=size_lines,
            antialiased=antialiased,
            raise_if_out_of_image=raise_if_out_of_image)
        if size_points <= 0:
            return heatmap_lines

        heatmap_points = self.draw_points_heatmap_array(
            image_shape,
            alpha=alpha_points,
            size=size_points,
            raise_if_out_of_image=raise_if_out_of_image)

        heatmap = np.dstack([heatmap_lines, heatmap_points])
        return np.max(heatmap, axis=2)