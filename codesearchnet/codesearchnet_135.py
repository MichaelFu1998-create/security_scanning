def draw_on_image(self, image, color=(0, 255, 0), alpha=1.0, size=1,
                      copy=True, raise_if_out_of_image=False, thickness=None):
        """
        Draw all bounding boxes onto a given image.

        Parameters
        ----------
        image : (H,W,3) ndarray
            The image onto which to draw the bounding boxes.
            This image should usually have the same shape as
            set in BoundingBoxesOnImage.shape.

        color : int or list of int or tuple of int or (3,) ndarray, optional
            The RGB color of all bounding boxes. If a single int ``C``, then
            that is equivalent to ``(C,C,C)``.

        alpha : float, optional
            Alpha/transparency of the bounding box.

        size : int, optional
            Thickness in pixels.

        copy : bool, optional
            Whether to copy the image before drawing the bounding boxes.

        raise_if_out_of_image : bool, optional
            Whether to raise an exception if any bounding box is outside of the
            image.

        thickness : None or int, optional
            Deprecated.

        Returns
        -------
        image : (H,W,3) ndarray
            Image with drawn bounding boxes.

        """
        image = np.copy(image) if copy else image

        for bb in self.bounding_boxes:
            image = bb.draw_on_image(
                image,
                color=color,
                alpha=alpha,
                size=size,
                copy=False,
                raise_if_out_of_image=raise_if_out_of_image,
                thickness=thickness
            )

        return image