def get_arr_int(self, background_threshold=0.01, background_class_id=None):
        """
        Get the segmentation map array as an integer array of shape (H, W).

        Each pixel in that array contains an integer value representing the pixel's class.
        If multiple classes overlap, the one with the highest local float value is picked.
        If that highest local value is below `background_threshold`, the method instead uses
        the background class id as the pixel's class value.
        By default, class id 0 is the background class. This may only be changed if the original
        input to the segmentation map object was an integer map.

        Parameters
        ----------
        background_threshold : float, optional
            At each pixel, each class-heatmap has a value between 0.0 and 1.0. If none of the
            class-heatmaps has a value above this threshold, the method uses the background class
            id instead.

        background_class_id : None or int, optional
            Class id to fall back to if no class-heatmap passes the threshold at a spatial
            location. May only be provided if the original input was an integer mask and in these
            cases defaults to 0. If the input were float or boolean masks, the background class id
            may not be set as it is assumed that the background is implicitly defined
            as 'any spatial location that has zero-like values in all masks'.

        Returns
        -------
        result : (H,W) ndarray
            Segmentation map array (int32).
            If the original input consisted of boolean or float masks, then the highest possible
            class id is ``1+C``, where ``C`` is the number of provided float/boolean masks. The value
            ``0`` in the integer mask then denotes the background class.

        """
        if self.input_was[0] in ["bool", "float"]:
            ia.do_assert(background_class_id is None,
                         "The background class id may only be changed if the original input to SegmentationMapOnImage "
                         + "was an *integer* based segmentation map.")

        if background_class_id is None:
            background_class_id = 0

        channelwise_max_idx = np.argmax(self.arr, axis=2)
        # for bool and float input masks, we assume that the background is implicitly given,
        # i.e. anything where all masks/channels have zero-like values
        # for int, we assume that the background class is explicitly given and has the index 0
        if self.input_was[0] in ["bool", "float"]:
            result = 1 + channelwise_max_idx
        else:  # integer mask was provided
            result = channelwise_max_idx
        if background_threshold is not None and background_threshold > 0:
            probs = np.amax(self.arr, axis=2)
            result[probs < background_threshold] = background_class_id

        return result.astype(np.int32)