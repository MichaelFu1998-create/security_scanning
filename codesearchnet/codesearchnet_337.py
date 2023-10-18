def max_pool(self, block_size):
        """
        Resize the heatmap(s) array using max-pooling of a given block/kernel size.

        Parameters
        ----------
        block_size : int or tuple of int
            Size of each block of values to pool, aka kernel size. See :func:`imgaug.pool` for details.

        Returns
        -------
        imgaug.HeatmapsOnImage
            Heatmaps after max-pooling.

        """
        arr_0to1_reduced = ia.max_pool(self.arr_0to1, block_size)
        return HeatmapsOnImage.from_0to1(arr_0to1_reduced, shape=self.shape, min_value=self.min_value,
                                         max_value=self.max_value)