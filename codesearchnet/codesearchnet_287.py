def draw_on_image(self, image,
                      color=(0, 255, 0), color_lines=None, color_points=None,
                      alpha=1.0, alpha_lines=None, alpha_points=None,
                      size=1, size_lines=None, size_points=None,
                      antialiased=True,
                      raise_if_out_of_image=False):
        """
        Draw the line string on an image.

        Parameters
        ----------
        image : ndarray
            The `(H,W,C)` `uint8` image onto which to draw the line string.

        color : iterable of int, optional
            Color to use as RGB, i.e. three values.
            The color of the line and points are derived from this value,
            unless they are set.

        color_lines : None or iterable of int
            Color to use for the line segments as RGB, i.e. three values.
            If ``None``, this value is derived from `color`.

        color_points : None or iterable of int
            Color to use for the points as RGB, i.e. three values.
            If ``None``, this value is derived from ``0.5 * color``.

        alpha : float, optional
            Opacity of the line string. Higher values denote more visible
            points.
            The alphas of the line and points are derived from this value,
            unless they are set.

        alpha_lines : None or float, optional
            Opacity of the line string. Higher values denote more visible
            line string.
            If ``None``, this value is derived from `alpha`.

        alpha_points : None or float, optional
            Opacity of the line string points. Higher values denote more
            visible points.
            If ``None``, this value is derived from `alpha`.

        size : int, optional
            Size of the line string.
            The sizes of the line and points are derived from this value,
            unless they are set.

        size_lines : None or int, optional
            Thickness of the line segments.
            If ``None``, this value is derived from `size`.

        size_points : None or int, optional
            Size of the points in pixels.
            If ``None``, this value is derived from ``3 * size``.

        antialiased : bool, optional
            Whether to draw the line with anti-aliasing activated.
            This does currently not affect the point drawing.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if the line string is fully
            outside of the image. If set to False, no error will be raised and
            only the parts inside the image will be drawn.

        Returns
        -------
        ndarray
            Image with line string drawn on it.

        """
        assert color is not None
        assert alpha is not None
        assert size is not None

        color_lines = color_lines if color_lines is not None \
            else np.float32(color)
        color_points = color_points if color_points is not None \
            else np.float32(color) * 0.5

        alpha_lines = alpha_lines if alpha_lines is not None \
            else np.float32(alpha)
        alpha_points = alpha_points if alpha_points is not None \
            else np.float32(alpha)

        size_lines = size_lines if size_lines is not None else size
        size_points = size_points if size_points is not None else size * 3

        image = self.draw_lines_on_image(
            image, color=np.array(color_lines).astype(np.uint8),
            alpha=alpha_lines, size=size_lines,
            antialiased=antialiased,
            raise_if_out_of_image=raise_if_out_of_image)

        image = self.draw_points_on_image(
            image, color=np.array(color_points).astype(np.uint8),
            alpha=alpha_points, size=size_points,
            copy=False,
            raise_if_out_of_image=raise_if_out_of_image)

        return image