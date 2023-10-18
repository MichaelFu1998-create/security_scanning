def draw_on_image(self, image, color=(0, 255, 0), alpha=1.0, size=3,
                      copy=True, raise_if_out_of_image=False):
        """
        Draw all keypoints onto a given image.

        Each keypoint is marked by a square of a chosen color and size.

        Parameters
        ----------
        image : (H,W,3) ndarray
            The image onto which to draw the keypoints.
            This image should usually have the same shape as
            set in KeypointsOnImage.shape.

        color : int or list of int or tuple of int or (3,) ndarray, optional
            The RGB color of all keypoints. If a single int ``C``, then that is
            equivalent to ``(C,C,C)``.

        alpha : float, optional
            The opacity of the drawn keypoint, where ``1.0`` denotes a fully
            visible keypoint and ``0.0`` an invisible one.

        size : int, optional
            The size of each point. If set to ``C``, each square will have
            size ``C x C``.

        copy : bool, optional
            Whether to copy the image before drawing the points.

        raise_if_out_of_image : bool, optional
            Whether to raise an exception if any keypoint is outside of the image.

        Returns
        -------
        image : (H,W,3) ndarray
            Image with drawn keypoints.

        """
        image = np.copy(image) if copy else image
        for keypoint in self.keypoints:
            image = keypoint.draw_on_image(
                image, color=color, alpha=alpha, size=size, copy=False,
                raise_if_out_of_image=raise_if_out_of_image)
        return image