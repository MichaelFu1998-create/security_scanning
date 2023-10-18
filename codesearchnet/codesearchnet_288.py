def extract_from_image(self, image, size=1, pad=True, pad_max=None,
                           antialiased=True, prevent_zero_size=True):
        """
        Extract the image pixels covered by the line string.

        It will only extract pixels overlapped by the line string.

        This function will by default zero-pad the image if the line string is
        partially/fully outside of the image. This is for consistency with
        the same implementations for bounding boxes and polygons.

        Parameters
        ----------
        image : ndarray
            The image of shape `(H,W,[C])` from which to extract the pixels
            within the line string.

        size : int, optional
            Thickness of the line.

        pad : bool, optional
            Whether to zero-pad the image if the object is partially/fully
            outside of it.

        pad_max : None or int, optional
            The maximum number of pixels that may be zero-paded on any side,
            i.e. if this has value ``N`` the total maximum of added pixels
            is ``4*N``.
            This option exists to prevent extremely large images as a result of
            single points being moved very far away during augmentation.

        antialiased : bool, optional
            Whether to apply anti-aliasing to the line string.

        prevent_zero_size : bool, optional
            Whether to prevent height or width of the extracted image from
            becoming zero. If this is set to True and height or width of the
            line string is below 1, the height/width will be increased to 1.
            This can be useful to prevent problems, e.g. with image saving or
            plotting. If it is set to False, images will be returned as
            ``(H', W')`` or ``(H', W', 3)`` with ``H`` or ``W`` potentially
            being 0.

        Returns
        -------
        image : (H',W') ndarray or (H',W',C) ndarray
            Pixels overlapping with the line string. Zero-padded if the
            line string is partially/fully outside of the image and
            ``pad=True``. If `prevent_zero_size` is activated, it is
            guarantueed that ``H'>0`` and ``W'>0``, otherwise only
            ``H'>=0`` and ``W'>=0``.

        """
        from .bbs import BoundingBox

        assert image.ndim in [2, 3], (
            "Expected image of shape (H,W,[C]), "
            "got shape %s." % (image.shape,))

        if len(self.coords) == 0 or size <= 0:
            if prevent_zero_size:
                return np.zeros((1, 1) + image.shape[2:], dtype=image.dtype)
            return np.zeros((0, 0) + image.shape[2:], dtype=image.dtype)

        xx = self.xx_int
        yy = self.yy_int

        # this would probably work if drawing was subpixel-accurate
        # x1 = np.min(self.coords[:, 0]) - (size / 2)
        # y1 = np.min(self.coords[:, 1]) - (size / 2)
        # x2 = np.max(self.coords[:, 0]) + (size / 2)
        # y2 = np.max(self.coords[:, 1]) + (size / 2)

        # this works currently with non-subpixel-accurate drawing
        sizeh = (size - 1) / 2
        x1 = np.min(xx) - sizeh
        y1 = np.min(yy) - sizeh
        x2 = np.max(xx) + 1 + sizeh
        y2 = np.max(yy) + 1 + sizeh
        bb = BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2)

        if len(self.coords) == 1:
            return bb.extract_from_image(image, pad=pad, pad_max=pad_max,
                                         prevent_zero_size=prevent_zero_size)

        heatmap = self.draw_lines_heatmap_array(
            image.shape[0:2], alpha=1.0, size=size, antialiased=antialiased)
        if image.ndim == 3:
            heatmap = np.atleast_3d(heatmap)
        image_masked = image.astype(np.float32) * heatmap
        extract = bb.extract_from_image(image_masked, pad=pad, pad_max=pad_max,
                                        prevent_zero_size=prevent_zero_size)
        return np.clip(np.round(extract), 0, 255).astype(np.uint8)