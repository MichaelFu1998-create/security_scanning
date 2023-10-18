def draw(self, size=None, cmap="jet"):
        """
        Render the heatmaps as RGB images.

        Parameters
        ----------
        size : None or float or iterable of int or iterable of float, optional
            Size of the rendered RGB image as ``(height, width)``.
            See :func:`imgaug.imgaug.imresize_single_image` for details.
            If set to None, no resizing is performed and the size of the heatmaps array is used.

        cmap : str or None, optional
            Color map of ``matplotlib`` to use in order to convert the heatmaps to RGB images.
            If set to None, no color map will be used and the heatmaps will be converted
            to simple intensity maps.

        Returns
        -------
        heatmaps_drawn : list of (H,W,3) ndarray
            Rendered heatmaps. One per heatmap array channel. Dtype is uint8.

        """
        heatmaps_uint8 = self.to_uint8()
        heatmaps_drawn = []

        for c in sm.xrange(heatmaps_uint8.shape[2]):
            # c:c+1 here, because the additional axis is needed by imresize_single_image
            heatmap_c = heatmaps_uint8[..., c:c+1]

            if size is not None:
                heatmap_c_rs = ia.imresize_single_image(heatmap_c, size, interpolation="nearest")
            else:
                heatmap_c_rs = heatmap_c
            heatmap_c_rs = np.squeeze(heatmap_c_rs).astype(np.float32) / 255.0

            if cmap is not None:
                # import only when necessary (faster startup; optional dependency; less fragile -- see issue #225)
                import matplotlib.pyplot as plt

                cmap_func = plt.get_cmap(cmap)
                heatmap_cmapped = cmap_func(heatmap_c_rs)
                heatmap_cmapped = np.delete(heatmap_cmapped, 3, 2)
            else:
                heatmap_cmapped = np.tile(heatmap_c_rs[..., np.newaxis], (1, 1, 3))

            heatmap_cmapped = np.clip(heatmap_cmapped * 255, 0, 255).astype(np.uint8)

            heatmaps_drawn.append(heatmap_cmapped)
        return heatmaps_drawn