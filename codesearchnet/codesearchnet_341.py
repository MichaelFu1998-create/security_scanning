def from_0to1(arr_0to1, shape, min_value=0.0, max_value=1.0):
        """
        Create a heatmaps object from an heatmap array containing values ranging from 0.0 to 1.0.

        Parameters
        ----------
        arr_0to1 : (H,W) or (H,W,C) ndarray
            Heatmap(s) array, where ``H`` is height, ``W`` is width and ``C`` is the number of heatmap channels.
            Expected dtype is float32.

        shape : tuple of ints
            Shape of the image on which the heatmap(s) is/are placed. NOT the shape of the
            heatmap(s) array, unless it is identical to the image shape (note the likely
            difference between the arrays in the number of channels).
            If there is not a corresponding image, use the shape of the heatmaps array.

        min_value : float, optional
            Minimum value for the heatmaps that the 0-to-1 array represents. This will usually
            be 0.0. It is used when calling :func:`imgaug.HeatmapsOnImage.get_arr`, which converts the
            underlying ``(0.0, 1.0)`` array to value range ``(min_value, max_value)``.
            E.g. if you started with heatmaps in the range ``(-1.0, 1.0)`` and projected these
            to (0.0, 1.0), you should call this function with ``min_value=-1.0``, ``max_value=1.0``
            so that :func:`imgaug.HeatmapsOnImage.get_arr` returns heatmap arrays having value
            range (-1.0, 1.0).

        max_value : float, optional
            Maximum value for the heatmaps that to 0-to-255 array represents.
            See parameter min_value for details.

        Returns
        -------
        heatmaps : imgaug.HeatmapsOnImage
            Heatmaps object.

        """
        heatmaps = HeatmapsOnImage(arr_0to1, shape, min_value=0.0, max_value=1.0)
        heatmaps.min_value = min_value
        heatmaps.max_value = max_value
        return heatmaps