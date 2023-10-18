def from_uint8(arr_uint8, shape, min_value=0.0, max_value=1.0):
        """
        Create a heatmaps object from an heatmap array containing values ranging from 0 to 255.

        Parameters
        ----------
        arr_uint8 : (H,W) ndarray or (H,W,C) ndarray
            Heatmap(s) array, where ``H`` is height, ``W`` is width and ``C`` is the number of heatmap channels.
            Expected dtype is uint8.

        shape : tuple of int
            Shape of the image on which the heatmap(s) is/are placed. NOT the shape of the
            heatmap(s) array, unless it is identical to the image shape (note the likely
            difference between the arrays in the number of channels).
            If there is not a corresponding image, use the shape of the heatmaps array.

        min_value : float, optional
            Minimum value for the heatmaps that the 0-to-255 array represents. This will usually
            be 0.0. It is used when calling :func:`imgaug.HeatmapsOnImage.get_arr`, which converts the
            underlying ``(0, 255)`` array to value range ``(min_value, max_value)``.

        max_value : float, optional
            Maximum value for the heatmaps that 0-to-255 array represents.
            See parameter `min_value` for details.

        Returns
        -------
        imgaug.HeatmapsOnImage
            Heatmaps object.

        """
        arr_0to1 = arr_uint8.astype(np.float32) / 255.0
        return HeatmapsOnImage.from_0to1(arr_0to1, shape, min_value=min_value, max_value=max_value)