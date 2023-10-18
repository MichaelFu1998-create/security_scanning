def draw_on_image(self, image, alpha=0.75, cmap="jet", resize="heatmaps"):
        """
        Draw the heatmaps as overlays over an image.

        Parameters
        ----------
        image : (H,W,3) ndarray
            Image onto which to draw the heatmaps. Expected to be of dtype uint8.

        alpha : float, optional
            Alpha/opacity value to use for the mixing of image and heatmaps.
            Higher values mean that the heatmaps will be more visible and the image less visible.

        cmap : str or None, optional
            Color map to use. See :func:`imgaug.HeatmapsOnImage.draw` for details.

        resize : {'heatmaps', 'image'}, optional
            In case of size differences between the image and heatmaps, either the image or
            the heatmaps can be resized. This parameter controls which of the two will be resized
            to the other's size.

        Returns
        -------
        mix : list of (H,W,3) ndarray
            Rendered overlays. One per heatmap array channel. Dtype is uint8.

        """
        # assert RGB image
        ia.do_assert(image.ndim == 3)
        ia.do_assert(image.shape[2] == 3)
        ia.do_assert(image.dtype.type == np.uint8)

        ia.do_assert(0 - 1e-8 <= alpha <= 1.0 + 1e-8)
        ia.do_assert(resize in ["heatmaps", "image"])

        if resize == "image":
            image = ia.imresize_single_image(image, self.arr_0to1.shape[0:2], interpolation="cubic")

        heatmaps_drawn = self.draw(
            size=image.shape[0:2] if resize == "heatmaps" else None,
            cmap=cmap
        )

        mix = [
            np.clip((1-alpha) * image + alpha * heatmap_i, 0, 255).astype(np.uint8)
            for heatmap_i
            in heatmaps_drawn
        ]

        return mix