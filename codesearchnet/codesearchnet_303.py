def draw_on_image(self, image,
                      color=(0, 255, 0), color_lines=None, color_points=None,
                      alpha=1.0, alpha_lines=None, alpha_points=None,
                      size=1, size_lines=None, size_points=None,
                      antialiased=True,
                      raise_if_out_of_image=False):
        """
        Draw all line strings onto a given image.

        Parameters
        ----------
        image : ndarray
            The `(H,W,C)` `uint8` image onto which to draw the line strings.

        color : iterable of int, optional
            Color to use as RGB, i.e. three values.
            The color of the lines and points are derived from this value,
            unless they are set.

        color_lines : None or iterable of int
            Color to use for the line segments as RGB, i.e. three values.
            If ``None``, this value is derived from `color`.

        color_points : None or iterable of int
            Color to use for the points as RGB, i.e. three values.
            If ``None``, this value is derived from ``0.5 * color``.

        alpha : float, optional
            Opacity of the line strings. Higher values denote more visible
            points.
            The alphas of the line and points are derived from this value,
            unless they are set.

        alpha_lines : None or float, optional
            Opacity of the line strings. Higher values denote more visible
            line string.
            If ``None``, this value is derived from `alpha`.

        alpha_points : None or float, optional
            Opacity of the line string points. Higher values denote more
            visible points.
            If ``None``, this value is derived from `alpha`.

        size : int, optional
            Size of the line strings.
            The sizes of the line and points are derived from this value,
            unless they are set.

        size_lines : None or int, optional
            Thickness of the line segments.
            If ``None``, this value is derived from `size`.

        size_points : None or int, optional
            Size of the points in pixels.
            If ``None``, this value is derived from ``3 * size``.

        antialiased : bool, optional
            Whether to draw the lines with anti-aliasing activated.
            This does currently not affect the point drawing.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if a line string is fully
            outside of the image. If set to False, no error will be raised and
            only the parts inside the image will be drawn.

        Returns
        -------
        ndarray
            Image with line strings drawn on it.

        """
        # TODO improve efficiency here by copying only once
        for ls in self.line_strings:
            image = ls.draw_on_image(
                image,
                color=color, color_lines=color_lines, color_points=color_points,
                alpha=alpha, alpha_lines=alpha_lines, alpha_points=alpha_points,
                size=size, size_lines=size_lines, size_points=size_points,
                antialiased=antialiased,
                raise_if_out_of_image=raise_if_out_of_image
            )

        return image