def draw_on_image(self,
                      image,
                      color=(0, 255, 0), color_face=None,
                      color_lines=None, color_points=None,
                      alpha=1.0, alpha_face=None,
                      alpha_lines=None, alpha_points=None,
                      size=1, size_lines=None, size_points=None,
                      raise_if_out_of_image=False):
        """
        Draw the polygon on an image.

        Parameters
        ----------
        image : (H,W,C) ndarray
            The image onto which to draw the polygon. Usually expected to be
            of dtype ``uint8``, though other dtypes are also handled.

        color : iterable of int, optional
            The color to use for the whole polygon.
            Must correspond to the channel layout of the image. Usually RGB.
            The values for `color_face`, `color_lines` and `color_points`
            will be derived from this color if they are set to ``None``.
            This argument has no effect if `color_face`, `color_lines`
            and `color_points` are all set anything other than ``None``.

        color_face : None or iterable of int, optional
            The color to use for the inner polygon area (excluding perimeter).
            Must correspond to the channel layout of the image. Usually RGB.
            If this is ``None``, it will be derived from ``color * 1.0``.

        color_lines : None or iterable of int, optional
            The color to use for the line (aka perimeter/border) of the polygon.
            Must correspond to the channel layout of the image. Usually RGB.
            If this is ``None``, it will be derived from ``color * 0.5``.

        color_points : None or iterable of int, optional
            The color to use for the corner points of the polygon.
            Must correspond to the channel layout of the image. Usually RGB.
            If this is ``None``, it will be derived from ``color * 0.5``.

        alpha : float, optional
            The opacity of the whole polygon, where ``1.0`` denotes a completely
            visible polygon and ``0.0`` an invisible one.
            The values for `alpha_face`, `alpha_lines` and `alpha_points`
            will be derived from this alpha value if they are set to ``None``.
            This argument has no effect if `alpha_face`, `alpha_lines`
            and `alpha_points` are all set anything other than ``None``.

        alpha_face : None or number, optional
            The opacity of the polygon's inner area (excluding the perimeter),
            where ``1.0`` denotes a completely visible inner area and ``0.0``
            an invisible one.
            If this is ``None``, it will be derived from ``alpha * 0.5``.

        alpha_lines : None or number, optional
            The opacity of the polygon's line (aka perimeter/border),
            where ``1.0`` denotes a completely visible line and ``0.0`` an
            invisible one.
            If this is ``None``, it will be derived from ``alpha * 1.0``.

        alpha_points : None or number, optional
            The opacity of the polygon's corner points, where ``1.0`` denotes
            completely visible corners and ``0.0`` invisible ones.
            If this is ``None``, it will be derived from ``alpha * 1.0``.

        size : int, optional
            Size of the polygon.
            The sizes of the line and points are derived from this value,
            unless they are set.

        size_lines : None or int, optional
            Thickness of the polygon's line (aka perimeter/border).
            If ``None``, this value is derived from `size`.

        size_points : int, optional
            Size of the points in pixels.
            If ``None``, this value is derived from ``3 * size``.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if the polygon is fully
            outside of the image. If set to False, no error will be raised and
            only the parts inside the image will be drawn.

        Returns
        -------
        result : (H,W,C) ndarray
            Image with polygon drawn on it. Result dtype is the same as the input dtype.

        """
        assert color is not None
        assert alpha is not None
        assert size is not None

        color_face = color_face if color_face is not None else np.array(color)
        color_lines = color_lines if color_lines is not None else np.array(color) * 0.5
        color_points = color_points if color_points is not None else np.array(color) * 0.5

        alpha_face = alpha_face if alpha_face is not None else alpha * 0.5
        alpha_lines = alpha_lines if alpha_lines is not None else alpha
        alpha_points = alpha_points if alpha_points is not None else alpha

        size_lines = size_lines if size_lines is not None else size
        size_points = size_points if size_points is not None else size * 3

        if image.ndim == 2:
            assert ia.is_single_number(color_face), (
                "Got a 2D image. Expected then 'color_face' to be a single "
                "number, but got %s." % (str(color_face),))
            color_face = [color_face]
        elif image.ndim == 3 and ia.is_single_number(color_face):
            color_face = [color_face] * image.shape[-1]

        if alpha_face < 0.01:
            alpha_face = 0
        elif alpha_face > 0.99:
            alpha_face = 1

        if raise_if_out_of_image and self.is_out_of_image(image):
            raise Exception("Cannot draw polygon %s on image with shape %s." % (
                str(self), image.shape
            ))

        # TODO np.clip to image plane if is_fully_within_image(), similar to how it is done for bounding boxes

        # TODO improve efficiency by only drawing in rectangle that covers poly instead of drawing in the whole image
        # TODO for a rectangular polygon, the face coordinates include the top/left boundary but not the right/bottom
        # boundary. This may be unintuitive when not drawing the boundary. Maybe somehow remove the boundary
        # coordinates from the face coordinates after generating both?
        input_dtype = image.dtype
        result = image.astype(np.float32)
        rr, cc = skimage.draw.polygon(self.yy_int, self.xx_int, shape=image.shape)
        if len(rr) > 0:
            if alpha_face == 1:
                result[rr, cc] = np.float32(color_face)
            elif alpha_face == 0:
                pass
            else:
                result[rr, cc] = (
                        (1 - alpha_face) * result[rr, cc, :]
                        + alpha_face * np.float32(color_face)
                )

        ls_open = self.to_line_string(closed=False)
        ls_closed = self.to_line_string(closed=True)
        result = ls_closed.draw_lines_on_image(
            result, color=color_lines, alpha=alpha_lines,
            size=size_lines, raise_if_out_of_image=raise_if_out_of_image)
        result = ls_open.draw_points_on_image(
            result, color=color_points, alpha=alpha_points,
            size=size_points, raise_if_out_of_image=raise_if_out_of_image)

        if input_dtype.type == np.uint8:
            result = np.clip(np.round(result), 0, 255).astype(input_dtype)  # TODO make clipping more flexible
        else:
            result = result.astype(input_dtype)

        return result