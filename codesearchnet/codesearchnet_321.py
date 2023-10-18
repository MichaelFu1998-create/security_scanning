def draw(self, size=None, background_threshold=0.01, background_class_id=None, colors=None,
             return_foreground_mask=False):
        """
        Render the segmentation map as an RGB image.

        Parameters
        ----------
        size : None or float or iterable of int or iterable of float, optional
            Size of the rendered RGB image as ``(height, width)``.
            See :func:`imgaug.imgaug.imresize_single_image` for details.
            If set to None, no resizing is performed and the size of the segmentation map array is used.

        background_threshold : float, optional
            See :func:`imgaug.SegmentationMapOnImage.get_arr_int`.

        background_class_id : None or int, optional
            See :func:`imgaug.SegmentationMapOnImage.get_arr_int`.

        colors : None or list of tuple of int, optional
            Colors to use. One for each class to draw. If None, then default colors will be used.

        return_foreground_mask : bool, optional
            Whether to return a mask of the same size as the drawn segmentation map, containing
            True at any spatial location that is not the background class and False everywhere else.

        Returns
        -------
        segmap_drawn : (H,W,3) ndarray
            Rendered segmentation map (dtype is uint8).

        foreground_mask : (H,W) ndarray
            Mask indicating the locations of foreground classes (dtype is bool).
            This value is only returned if `return_foreground_mask` is True.

        """
        arr = self.get_arr_int(background_threshold=background_threshold, background_class_id=background_class_id)
        nb_classes = 1 + np.max(arr)
        segmap_drawn = np.zeros((arr.shape[0], arr.shape[1], 3), dtype=np.uint8)
        if colors is None:
            colors = SegmentationMapOnImage.DEFAULT_SEGMENT_COLORS
        ia.do_assert(nb_classes <= len(colors),
                     "Can't draw all %d classes as it would exceed the maximum number of %d available colors." % (
                         nb_classes, len(colors),))

        ids_in_map = np.unique(arr)
        for c, color in zip(sm.xrange(nb_classes), colors):
            if c in ids_in_map:
                class_mask = (arr == c)
                segmap_drawn[class_mask] = color

        if return_foreground_mask:
            background_class_id = 0 if background_class_id is None else background_class_id
            foreground_mask = (arr != background_class_id)
        else:
            foreground_mask = None

        if size is not None:
            segmap_drawn = ia.imresize_single_image(segmap_drawn, size, interpolation="nearest")
            if foreground_mask is not None:
                foreground_mask = ia.imresize_single_image(
                    foreground_mask.astype(np.uint8), size, interpolation="nearest") > 0

        if foreground_mask is not None:
            return segmap_drawn, foreground_mask
        return segmap_drawn