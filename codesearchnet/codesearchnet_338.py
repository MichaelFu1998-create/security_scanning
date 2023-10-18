def resize(self, sizes, interpolation="cubic"):
        """
        Resize the heatmap(s) array to the provided size given the provided interpolation.

        Parameters
        ----------
        sizes : float or iterable of int or iterable of float
            New size of the array in ``(height, width)``.
            See :func:`imgaug.imgaug.imresize_single_image` for details.

        interpolation : None or str or int, optional
            The interpolation to use during resize.
            See :func:`imgaug.imgaug.imresize_single_image` for details.

        Returns
        -------
        imgaug.HeatmapsOnImage
            Resized heatmaps object.

        """
        arr_0to1_resized = ia.imresize_single_image(self.arr_0to1, sizes, interpolation=interpolation)

        # cubic interpolation can lead to values outside of [0.0, 1.0],
        # see https://github.com/opencv/opencv/issues/7195
        # TODO area interpolation too?
        arr_0to1_resized = np.clip(arr_0to1_resized, 0.0, 1.0)

        return HeatmapsOnImage.from_0to1(arr_0to1_resized, shape=self.shape, min_value=self.min_value,
                                         max_value=self.max_value)