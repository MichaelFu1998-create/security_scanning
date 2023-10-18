def draw_points_on_image(self, image, color=(0, 128, 0),
                             alpha=1.0, size=3,
                             copy=True, raise_if_out_of_image=False):
        """
        Draw the points of the line string on a given image.

        Parameters
        ----------
        image : ndarray or tuple of int
            The image onto which to draw.
            Expected to be ``uint8`` and of shape ``(H, W, C)`` with ``C``
            usually being ``3`` (other values are not tested).
            If a tuple, expected to be ``(H, W, C)`` and will lead to a new
            ``uint8`` array of zeros being created.

        color : iterable of int
            Color to use as RGB, i.e. three values.

        alpha : float, optional
            Opacity of the line string points. Higher values denote a more
            visible points.

        size : int, optional
            Size of the points in pixels.

        copy : bool, optional
            Whether it is allowed to draw directly in the input
            array (``False``) or it has to be copied (``True``).
            The routine may still have to copy, even if ``copy=False`` was
            used. Always use the return value.

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
        from .kps import KeypointsOnImage
        kpsoi = KeypointsOnImage.from_xy_array(self.coords, shape=image.shape)
        image = kpsoi.draw_on_image(
            image, color=color, alpha=alpha,
            size=size, copy=copy,
            raise_if_out_of_image=raise_if_out_of_image)

        return image