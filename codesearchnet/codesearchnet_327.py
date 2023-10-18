def from_heatmaps(heatmaps, class_indices=None, nb_classes=None):
        """
        Convert heatmaps to segmentation map.

        Assumes that each class is represented as a single heatmap channel.

        Parameters
        ----------
        heatmaps : imgaug.HeatmapsOnImage
            Heatmaps to convert.

        class_indices : None or list of int, optional
            List of class indices represented by each heatmap channel. See also the
            secondary output of :func:`imgaug.SegmentationMapOnImage.to_heatmap`.
            If this is provided, it must have the same length as the number of heatmap channels.

        nb_classes : None or int, optional
            Number of classes. Must be provided if class_indices is set.

        Returns
        -------
        imgaug.SegmentationMapOnImage
            Segmentation map derived from heatmaps.

        """
        if class_indices is None:
            return SegmentationMapOnImage(heatmaps.arr_0to1, shape=heatmaps.shape)
        else:
            ia.do_assert(nb_classes is not None)
            ia.do_assert(min(class_indices) >= 0)
            ia.do_assert(max(class_indices) < nb_classes)
            ia.do_assert(len(class_indices) == heatmaps.arr_0to1.shape[2])
            arr_0to1 = heatmaps.arr_0to1
            arr_0to1_full = np.zeros((arr_0to1.shape[0], arr_0to1.shape[1], nb_classes), dtype=np.float32)
            for heatmap_channel, mapped_channel in enumerate(class_indices):
                arr_0to1_full[:, :, mapped_channel] = arr_0to1[:, :, heatmap_channel]
            return SegmentationMapOnImage(arr_0to1_full, shape=heatmaps.shape)