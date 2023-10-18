def to_heatmaps(self, only_nonempty=False, not_none_if_no_nonempty=False):
        """
        Convert segmentation map to heatmaps object.

        Each segmentation map class will be represented as a single heatmap channel.

        Parameters
        ----------
        only_nonempty : bool, optional
            If True, then only heatmaps for classes that appear in the segmentation map will be
            generated. Additionally, a list of these class ids will be returned.

        not_none_if_no_nonempty : bool, optional
            If `only_nonempty` is True and for a segmentation map no channel was non-empty,
            this function usually returns None as the heatmaps object. If however this parameter
            is set to True, a heatmaps object with one channel (representing class 0)
            will be returned as a fallback in these cases.

        Returns
        -------
        imgaug.HeatmapsOnImage or None
            Segmentation map as a heatmaps object.
            If `only_nonempty` was set to True and no class appeared in the segmentation map,
            then this is None.

        class_indices : list of int
            Class ids (0 to C-1) of the classes that were actually added to the heatmaps.
            Only returned if `only_nonempty` was set to True.

        """
        # TODO get rid of this deferred import
        from imgaug.augmentables.heatmaps import HeatmapsOnImage

        if not only_nonempty:
            return HeatmapsOnImage.from_0to1(self.arr, self.shape, min_value=0.0, max_value=1.0)
        else:
            nonempty_mask = np.sum(self.arr, axis=(0, 1)) > 0 + 1e-4
            if np.sum(nonempty_mask) == 0:
                if not_none_if_no_nonempty:
                    nonempty_mask[0] = True
                else:
                    return None, []

            class_indices = np.arange(self.arr.shape[2])[nonempty_mask]
            channels = self.arr[..., class_indices]
            return HeatmapsOnImage(channels, self.shape, min_value=0.0, max_value=1.0), class_indices