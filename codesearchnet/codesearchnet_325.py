def resize(self, sizes, interpolation="cubic"):
        """
        Resize the segmentation map array to the provided size given the provided interpolation.

        Parameters
        ----------
        sizes : float or iterable of int or iterable of float
            New size of the array in ``(height, width)``.
            See :func:`imgaug.imgaug.imresize_single_image` for details.

        interpolation : None or str or int, optional
            The interpolation to use during resize.
            See :func:`imgaug.imgaug.imresize_single_image` for details.
            Note: The segmentation map is internally stored as multiple float-based heatmaps,
            making smooth interpolations potentially more reasonable than nearest neighbour
            interpolation.

        Returns
        -------
        segmap : imgaug.SegmentationMapOnImage
            Resized segmentation map object.

        """
        arr_resized = ia.imresize_single_image(self.arr, sizes, interpolation=interpolation)

        # cubic interpolation can lead to values outside of [0.0, 1.0],
        # see https://github.com/opencv/opencv/issues/7195
        # TODO area interpolation too?
        arr_resized = np.clip(arr_resized, 0.0, 1.0)
        segmap = SegmentationMapOnImage(arr_resized, shape=self.shape)
        segmap.input_was = self.input_was
        return segmap