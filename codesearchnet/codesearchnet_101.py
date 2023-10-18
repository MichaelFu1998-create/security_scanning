def draw_on_image(self, image, color=(0, 255, 0), alpha=1.0, size=3,
                      copy=True, raise_if_out_of_image=False):
        """
        Draw the keypoint onto a given image.

        The keypoint is drawn as a square.

        Parameters
        ----------
        image : (H,W,3) ndarray
            The image onto which to draw the keypoint.

        color : int or list of int or tuple of int or (3,) ndarray, optional
            The RGB color of the keypoint. If a single int ``C``, then that is
            equivalent to ``(C,C,C)``.

        alpha : float, optional
            The opacity of the drawn keypoint, where ``1.0`` denotes a fully
            visible keypoint and ``0.0`` an invisible one.

        size : int, optional
            The size of the keypoint. If set to ``S``, each square will have
            size ``S x S``.

        copy : bool, optional
            Whether to copy the image before drawing the keypoint.

        raise_if_out_of_image : bool, optional
            Whether to raise an exception if the keypoint is outside of the
            image.

        Returns
        -------
        image : (H,W,3) ndarray
            Image with drawn keypoint.

        """
        if copy:
            image = np.copy(image)

        if image.ndim == 2:
            assert ia.is_single_number(color), (
                "Got a 2D image. Expected then 'color' to be a single number, "
                "but got %s." % (str(color),))
        elif image.ndim == 3 and ia.is_single_number(color):
            color = [color] * image.shape[-1]

        input_dtype = image.dtype
        alpha_color = color
        if alpha < 0.01:
            # keypoint invisible, nothing to do
            return image
        elif alpha > 0.99:
            alpha = 1
        else:
            image = image.astype(np.float32, copy=False)
            alpha_color = alpha * np.array(color)

        height, width = image.shape[0:2]

        y, x = self.y_int, self.x_int

        x1 = max(x - size//2, 0)
        x2 = min(x + 1 + size//2, width)
        y1 = max(y - size//2, 0)
        y2 = min(y + 1 + size//2, height)

        x1_clipped, x2_clipped = np.clip([x1, x2], 0, width)
        y1_clipped, y2_clipped = np.clip([y1, y2], 0, height)

        x1_clipped_ooi = (x1_clipped < 0 or x1_clipped >= width)
        x2_clipped_ooi = (x2_clipped < 0 or x2_clipped >= width+1)
        y1_clipped_ooi = (y1_clipped < 0 or y1_clipped >= height)
        y2_clipped_ooi = (y2_clipped < 0 or y2_clipped >= height+1)
        x_ooi = (x1_clipped_ooi and x2_clipped_ooi)
        y_ooi = (y1_clipped_ooi and y2_clipped_ooi)
        x_zero_size = (x2_clipped - x1_clipped) < 1  # min size is 1px
        y_zero_size = (y2_clipped - y1_clipped) < 1
        if not x_ooi and not y_ooi and not x_zero_size and not y_zero_size:
            if alpha == 1:
                image[y1_clipped:y2_clipped, x1_clipped:x2_clipped] = color
            else:
                image[y1_clipped:y2_clipped, x1_clipped:x2_clipped] = (
                        (1 - alpha)
                        * image[y1_clipped:y2_clipped, x1_clipped:x2_clipped]
                        + alpha_color
                )
        else:
            if raise_if_out_of_image:
                raise Exception(
                    "Cannot draw keypoint x=%.8f, y=%.8f on image with "
                    "shape %s." % (y, x, image.shape))

        if image.dtype.name != input_dtype.name:
            if input_dtype.name == "uint8":
                image = np.clip(image, 0, 255, out=image)
            image = image.astype(input_dtype, copy=False)
        return image