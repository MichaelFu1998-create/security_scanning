def draw_on_image(self, image, alpha=0.75, resize="segmentation_map", background_threshold=0.01,
                      background_class_id=None, colors=None, draw_background=False):
        """
        Draw the segmentation map as an overlay over an image.

        Parameters
        ----------
        image : (H,W,3) ndarray
            Image onto which to draw the segmentation map. Dtype is expected to be uint8.

        alpha : float, optional
            Alpha/opacity value to use for the mixing of image and segmentation map.
            Higher values mean that the segmentation map will be more visible and the image less visible.

        resize : {'segmentation_map', 'image'}, optional
            In case of size differences between the image and segmentation map, either the image or
            the segmentation map can be resized. This parameter controls which of the two will be
            resized to the other's size.

        background_threshold : float, optional
            See :func:`imgaug.SegmentationMapOnImage.get_arr_int`.

        background_class_id : None or int, optional
            See :func:`imgaug.SegmentationMapOnImage.get_arr_int`.

        colors : None or list of tuple of int, optional
            Colors to use. One for each class to draw. If None, then default colors will be used.

        draw_background : bool, optional
            If True, the background will be drawn like any other class.
            If False, the background will not be drawn, i.e. the respective background pixels
            will be identical with the image's RGB color at the corresponding spatial location
            and no color overlay will be applied.

        Returns
        -------
        mix : (H,W,3) ndarray
            Rendered overlays (dtype is uint8).

        """
        # assert RGB image
        ia.do_assert(image.ndim == 3)
        ia.do_assert(image.shape[2] == 3)
        ia.do_assert(image.dtype.type == np.uint8)

        ia.do_assert(0 - 1e-8 <= alpha <= 1.0 + 1e-8)
        ia.do_assert(resize in ["segmentation_map", "image"])

        if resize == "image":
            image = ia.imresize_single_image(image, self.arr.shape[0:2], interpolation="cubic")

        segmap_drawn, foreground_mask = self.draw(
            background_threshold=background_threshold,
            background_class_id=background_class_id,
            size=image.shape[0:2] if resize == "segmentation_map" else None,
            colors=colors,
            return_foreground_mask=True
        )

        if draw_background:
            mix = np.clip(
                (1-alpha) * image + alpha * segmap_drawn,
                0,
                255
            ).astype(np.uint8)
        else:
            foreground_mask = foreground_mask[..., np.newaxis]
            mix = np.zeros_like(image)
            mix += (~foreground_mask).astype(np.uint8) * image
            mix += foreground_mask.astype(np.uint8) * np.clip(
                (1-alpha) * image + alpha * segmap_drawn,
                0,
                255
            ).astype(np.uint8)
        return mix