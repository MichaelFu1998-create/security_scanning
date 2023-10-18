def invert(self):
        """
        Inverts each value in the heatmap, shifting low towards high values and vice versa.

        This changes each value to::

            v' = max - (v - min)

        where ``v`` is the value at some spatial location, ``min`` is the minimum value in the heatmap
        and ``max`` is the maximum value.
        As the heatmap uses internally a 0.0 to 1.0 representation, this simply becomes ``v' = 1.0 - v``.

        Note that the attributes ``min_value`` and ``max_value`` are not switched. They both keep their values.

        This function can be useful e.g. when working with depth maps, where algorithms might have
        an easier time representing the furthest away points with zeros, requiring an inverted
        depth map.

        Returns
        -------
        arr_inv : imgaug.HeatmapsOnImage
            Inverted heatmap.

        """
        arr_inv = HeatmapsOnImage.from_0to1(1 - self.arr_0to1, shape=self.shape, min_value=self.min_value,
                                            max_value=self.max_value)
        arr_inv.arr_was_2d = self.arr_was_2d
        return arr_inv