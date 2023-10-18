def get_arr(self):
        """
        Get the heatmap's array within the value range originally provided in ``__init__()``.

        The HeatmapsOnImage object saves heatmaps internally in the value range ``(min=0.0, max=1.0)``.
        This function converts the internal representation to ``(min=min_value, max=max_value)``,
        where ``min_value`` and ``max_value`` are provided upon instantiation of the object.

        Returns
        -------
        result : (H,W) ndarray or (H,W,C) ndarray
            Heatmap array. Dtype is float32.

        """
        if self.arr_was_2d and self.arr_0to1.shape[2] == 1:
            arr = self.arr_0to1[:, :, 0]
        else:
            arr = self.arr_0to1

        eps = np.finfo(np.float32).eps
        min_is_zero = 0.0 - eps < self.min_value < 0.0 + eps
        max_is_one = 1.0 - eps < self.max_value < 1.0 + eps
        if min_is_zero and max_is_one:
            return np.copy(arr)
        else:
            diff = self.max_value - self.min_value
            return self.min_value + diff * arr