def extract_from_image(self, image, pad=True, pad_max=None,
                           prevent_zero_size=True):
        """
        Extract the image pixels within the bounding box.

        This function will zero-pad the image if the bounding box is partially/fully outside of
        the image.

        Parameters
        ----------
        image : (H,W) ndarray or (H,W,C) ndarray
            The image from which to extract the pixels within the bounding box.

        pad : bool, optional
            Whether to zero-pad the image if the object is partially/fully
            outside of it.

        pad_max : None or int, optional
            The maximum number of pixels that may be zero-paded on any side,
            i.e. if this has value ``N`` the total maximum of added pixels
            is ``4*N``.
            This option exists to prevent extremely large images as a result of
            single points being moved very far away during augmentation.

        prevent_zero_size : bool, optional
            Whether to prevent height or width of the extracted image from becoming zero.
            If this is set to True and height or width of the bounding box is below 1, the height/width will
            be increased to 1. This can be useful to prevent problems, e.g. with image saving or plotting.
            If it is set to False, images will be returned as ``(H', W')`` or ``(H', W', 3)`` with ``H`` or
            ``W`` potentially being 0.

        Returns
        -------
        image : (H',W') ndarray or (H',W',C) ndarray
            Pixels within the bounding box. Zero-padded if the bounding box is partially/fully
            outside of the image. If prevent_zero_size is activated, it is guarantueed that ``H'>0``
            and ``W'>0``, otherwise only ``H'>=0`` and ``W'>=0``.

        """
        pad_top = 0
        pad_right = 0
        pad_bottom = 0
        pad_left = 0

        height, width = image.shape[0], image.shape[1]
        x1, x2, y1, y2 = self.x1_int, self.x2_int, self.y1_int, self.y2_int

        # When y values get into the range (H-0.5, H), the *_int functions round them to H.
        # That is technically sensible, but in the case of extraction leads to a black border,
        # which is both ugly and unexpected after calling cut_out_of_image(). Here we correct for
        # that because of beauty reasons.
        # Same is the case for x coordinates.
        fully_within = self.is_fully_within_image(image)
        if fully_within:
            y1, y2 = np.clip([y1, y2], 0, height-1)
            x1, x2 = np.clip([x1, x2], 0, width-1)

        # TODO add test
        if prevent_zero_size:
            if abs(x2 - x1) < 1:
                x2 = x1 + 1
            if abs(y2 - y1) < 1:
                y2 = y1 + 1

        if pad:
            # if the bb is outside of the image area, the following pads the image
            # first with black pixels until the bb is inside the image
            # and only then extracts the image area
            # TODO probably more efficient to initialize an array of zeros
            # and copy only the portions of the bb into that array that are
            # natively inside the image area
            if x1 < 0:
                pad_left = abs(x1)
                x2 = x2 + pad_left
                width = width + pad_left
                x1 = 0
            if y1 < 0:
                pad_top = abs(y1)
                y2 = y2 + pad_top
                height = height + pad_top
                y1 = 0
            if x2 >= width:
                pad_right = x2 - width
            if y2 >= height:
                pad_bottom = y2 - height

            paddings = [pad_top, pad_right, pad_bottom, pad_left]
            any_padded = any([val > 0 for val in paddings])
            if any_padded:
                if pad_max is None:
                    pad_max = max(paddings)

                image = ia.pad(
                    image,
                    top=min(pad_top, pad_max),
                    right=min(pad_right, pad_max),
                    bottom=min(pad_bottom, pad_max),
                    left=min(pad_left, pad_max)
                )
            return image[y1:y2, x1:x2]
        else:
            within_image = (
                (0, 0, 0, 0)
                <= (x1, y1, x2, y2)
                < (width, height, width, height)
            )
            out_height, out_width = (y2 - y1), (x2 - x1)
            nonzero_height = (out_height > 0)
            nonzero_width = (out_width > 0)
            if within_image and nonzero_height and nonzero_width:
                return image[y1:y2, x1:x2]
            if prevent_zero_size:
                out_height = 1
                out_width = 1
            else:
                out_height = 0
                out_width = 0
            if image.ndim == 2:
                return np.zeros((out_height, out_width), dtype=image.dtype)
            return np.zeros((out_height, out_width, image.shape[-1]),
                            dtype=image.dtype)