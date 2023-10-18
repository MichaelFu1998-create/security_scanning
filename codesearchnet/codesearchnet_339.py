def to_uint8(self):
        """
        Convert this heatmaps object to a 0-to-255 array.

        Returns
        -------
        arr_uint8 : (H,W,C) ndarray
            Heatmap as a 0-to-255 array (dtype is uint8).

        """
        # TODO this always returns (H,W,C), even if input ndarray was originall (H,W)
        # does it make sense here to also return (H,W) if self.arr_was_2d?
        arr_0to255 = np.clip(np.round(self.arr_0to1 * 255), 0, 255)
        arr_uint8 = arr_0to255.astype(np.uint8)
        return arr_uint8