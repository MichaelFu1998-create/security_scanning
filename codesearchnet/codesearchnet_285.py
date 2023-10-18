def draw_lines_on_image(self, image, color=(0, 255, 0),
                            alpha=1.0, size=3,
                            antialiased=True,
                            raise_if_out_of_image=False):
        """
        Draw the line segments of the line string on a given image.

        Parameters
        ----------
        image : ndarray or tuple of int
            The image onto which to draw.
            Expected to be ``uint8`` and of shape ``(H, W, C)`` with ``C``
            usually being ``3`` (other values are not tested).
            If a tuple, expected to be ``(H, W, C)`` and will lead to a new
            ``uint8`` array of zeros being created.

        color : int or iterable of int
            Color to use as RGB, i.e. three values.

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
            `image` with line drawn on it.

        """
        from .. import dtypes as iadt
        from ..augmenters import blend as blendlib

        image_was_empty = False
        if isinstance(image, tuple):
            image_was_empty = True
            image = np.zeros(image, dtype=np.uint8)
        assert image.ndim in [2, 3], (
            ("Expected image or shape of form (H,W) or (H,W,C), "
             + "got shape %s.") % (image.shape,))

        if len(self.coords) <= 1 or alpha < 0 + 1e-4 or size < 1:
            return np.copy(image)

        if raise_if_out_of_image \
                and self.is_out_of_image(image, partly=False, fully=True):
            raise Exception(
                "Cannot draw line string '%s' on image with shape %s, because "
                "it would be out of bounds." % (
                    self.__str__(), image.shape))

        if image.ndim == 2:
            assert ia.is_single_number(color), (
                "Got a 2D image. Expected then 'color' to be a single number, "
                "but got %s." % (str(color),))
            color = [color]
        elif image.ndim == 3 and ia.is_single_number(color):
            color = [color] * image.shape[-1]

        image = image.astype(np.float32)
        height, width = image.shape[0:2]

        # We can't trivially exclude lines outside of the image here, because
        # even if start and end point are outside, there can still be parts of
        # the line inside the image.
        # TODO Do this with edge-wise intersection tests
        lines = []
        for line_start, line_end in zip(self.coords[:-1], self.coords[1:]):
            # note that line() expects order (y1, x1, y2, x2), hence ([1], [0])
            lines.append((line_start[1], line_start[0],
                          line_end[1], line_end[0]))

        # skimage.draw.line can only handle integers
        lines = np.round(np.float32(lines)).astype(np.int32)

        # size == 0 is already covered above
        # Note here that we have to be careful not to draw lines two times
        # at their intersection points, e.g. for (p0, p1), (p1, 2) we could
        # end up drawing at p1 twice, leading to higher values if alpha is used.
        color = np.float32(color)
        heatmap = np.zeros(image.shape[0:2], dtype=np.float32)
        for line in lines:
            if antialiased:
                rr, cc, val = skimage.draw.line_aa(*line)
            else:
                rr, cc = skimage.draw.line(*line)
                val = 1.0

            # mask check here, because line() can generate coordinates
            # outside of the image plane
            rr_mask = np.logical_and(0 <= rr, rr < height)
            cc_mask = np.logical_and(0 <= cc, cc < width)
            mask = np.logical_and(rr_mask, cc_mask)

            if np.any(mask):
                rr = rr[mask]
                cc = cc[mask]
                val = val[mask] if not ia.is_single_number(val) else val
                heatmap[rr, cc] = val * alpha

        if size > 1:
            kernel = np.ones((size, size), dtype=np.uint8)
            heatmap = cv2.dilate(heatmap, kernel)

        if image_was_empty:
            image_blend = image + heatmap * color
        else:
            image_color_shape = image.shape[0:2]
            if image.ndim == 3:
                image_color_shape = image_color_shape + (1,)
            image_color = np.tile(color, image_color_shape)
            image_blend = blendlib.blend_alpha(image_color, image, heatmap)

        image_blend = iadt.restore_dtypes_(image_blend, np.uint8)
        return image_blend