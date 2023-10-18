def draw_on_image(self, image, color=(0, 255, 0), alpha=1.0, size=1,
                      copy=True, raise_if_out_of_image=False, thickness=None):
        """
        Draw the bounding box on an image.

        Parameters
        ----------
        image : (H,W,C) ndarray(uint8)
            The image onto which to draw the bounding box.

        color : iterable of int, optional
            The color to use, corresponding to the channel layout of the image. Usually RGB.

        alpha : float, optional
            The transparency of the drawn bounding box, where 1.0 denotes no transparency and
            0.0 is invisible.

        size : int, optional
            The thickness of the bounding box in pixels. If the value is larger than 1, then
            additional pixels will be added around the bounding box (i.e. extension towards the
            outside).

        copy : bool, optional
            Whether to copy the input image or change it in-place.

        raise_if_out_of_image : bool, optional
            Whether to raise an error if the bounding box is fully outside of the
            image. If set to False, no error will be raised and only the parts inside the image
            will be drawn.

        thickness : None or int, optional
            Deprecated.

        Returns
        -------
        result : (H,W,C) ndarray(uint8)
            Image with bounding box drawn on it.

        """
        if thickness is not None:
            ia.warn_deprecated(
                "Usage of argument 'thickness' in BoundingBox.draw_on_image() "
                "is deprecated. The argument was renamed to 'size'."
            )
            size = thickness

        if raise_if_out_of_image and self.is_out_of_image(image):
            raise Exception("Cannot draw bounding box x1=%.8f, y1=%.8f, x2=%.8f, y2=%.8f on image with shape %s." % (
                self.x1, self.y1, self.x2, self.y2, image.shape))

        result = np.copy(image) if copy else image

        if isinstance(color, (tuple, list)):
            color = np.uint8(color)

        for i in range(size):
            y1, y2, x1, x2 = self.y1_int, self.y2_int, self.x1_int, self.x2_int

            # When y values get into the range (H-0.5, H), the *_int functions round them to H.
            # That is technically sensible, but in the case of drawing means that the border lies
            # just barely outside of the image, making the border disappear, even though the BB
            # is fully inside the image. Here we correct for that because of beauty reasons.
            # Same is the case for x coordinates.
            if self.is_fully_within_image(image):
                y1 = np.clip(y1, 0, image.shape[0]-1)
                y2 = np.clip(y2, 0, image.shape[0]-1)
                x1 = np.clip(x1, 0, image.shape[1]-1)
                x2 = np.clip(x2, 0, image.shape[1]-1)

            y = [y1-i, y1-i, y2+i, y2+i]
            x = [x1-i, x2+i, x2+i, x1-i]
            rr, cc = skimage.draw.polygon_perimeter(y, x, shape=result.shape)
            if alpha >= 0.99:
                result[rr, cc, :] = color
            else:
                if ia.is_float_array(result):
                    result[rr, cc, :] = (1 - alpha) * result[rr, cc, :] + alpha * color
                    result = np.clip(result, 0, 255)
                else:
                    input_dtype = result.dtype
                    result = result.astype(np.float32)
                    result[rr, cc, :] = (1 - alpha) * result[rr, cc, :] + alpha * color
                    result = np.clip(result, 0, 255).astype(input_dtype)

        return result