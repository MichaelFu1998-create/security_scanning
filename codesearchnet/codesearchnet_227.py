def draw_on_image(self,
                      image,
                      color=(0, 255, 0), color_face=None,
                      color_lines=None, color_points=None,
                      alpha=1.0, alpha_face=None,
                      alpha_lines=None, alpha_points=None,
                      size=1, size_lines=None, size_points=None,
                      raise_if_out_of_image=False):
        """
        Draw all polygons onto a given image.

        Parameters
        ----------
        image : (H,W,C) ndarray
            The image onto which to draw the bounding boxes.
            This image should usually have the same shape as set in
            ``PolygonsOnImage.shape``.

        color : iterable of int, optional
            The color to use for the whole polygons.
            Must correspond to the channel layout of the image. Usually RGB.
            The values for `color_face`, `color_lines` and `color_points`
            will be derived from this color if they are set to ``None``.
            This argument has no effect if `color_face`, `color_lines`
            and `color_points` are all set anything other than ``None``.

        color_face : None or iterable of int, optional
            The color to use for the inner polygon areas (excluding perimeters).
            Must correspond to the channel layout of the image. Usually RGB.
            If this is ``None``, it will be derived from ``color * 1.0``.

        color_lines : None or iterable of int, optional
            The color to use for the lines (aka perimeters/borders) of the
            polygons. Must correspond to the channel layout of the image.
            Usually RGB. If this is ``None``, it will be derived
            from ``color * 0.5``.

        color_points : None or iterable of int, optional
            The color to use for the corner points of the polygons.
            Must correspond to the channel layout of the image. Usually RGB.
            If this is ``None``, it will be derived from ``color * 0.5``.

        alpha : float, optional
            The opacity of the whole polygons, where ``1.0`` denotes
            completely visible polygons and ``0.0`` invisible ones.
            The values for `alpha_face`, `alpha_lines` and `alpha_points`
            will be derived from this alpha value if they are set to ``None``.
            This argument has no effect if `alpha_face`, `alpha_lines`
            and `alpha_points` are all set anything other than ``None``.

        alpha_face : None or number, optional
            The opacity of the polygon's inner areas (excluding the perimeters),
            where ``1.0`` denotes completely visible inner areas and ``0.0``
            invisible ones.
            If this is ``None``, it will be derived from ``alpha * 0.5``.

        alpha_lines : None or number, optional
            The opacity of the polygon's lines (aka perimeters/borders),
            where ``1.0`` denotes completely visible perimeters and ``0.0``
            invisible ones.
            If this is ``None``, it will be derived from ``alpha * 1.0``.

        alpha_points : None or number, optional
            The opacity of the polygon's corner points, where ``1.0`` denotes
            completely visible corners and ``0.0`` invisible ones.
            Currently this is an on/off choice, i.e. only ``0.0`` or ``1.0``
            are allowed.
            If this is ``None``, it will be derived from ``alpha * 1.0``.

        size : int, optional
            Size of the polygons.
            The sizes of the line and points are derived from this value,
            unless they are set.

        size_lines : None or int, optional
            Thickness of the polygon lines (aka perimeter/border).
            If ``None``, this value is derived from `size`.

        size_points : int, optional
            The size of all corner points. If set to ``C``, each corner point
            will be drawn as a square of size ``C x C``.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if any polygon is fully
            outside of the image. If set to False, no error will be raised and
            only the parts inside the image will be drawn.

        Returns
        -------
        image : (H,W,C) ndarray
            Image with drawn polygons.

        """
        for poly in self.polygons:
            image = poly.draw_on_image(
                image,
                color=color,
                color_face=color_face,
                color_lines=color_lines,
                color_points=color_points,
                alpha=alpha,
                alpha_face=alpha_face,
                alpha_lines=alpha_lines,
                alpha_points=alpha_points,
                size=size,
                size_lines=size_lines,
                size_points=size_points,
                raise_if_out_of_image=raise_if_out_of_image
            )
        return image