def change_normalization(cls, arr, source, target):
        """
        Change the value range of a heatmap from one min-max to another min-max.

        E.g. the value range may be changed from min=0.0, max=1.0 to min=-1.0, max=1.0.

        Parameters
        ----------
        arr : ndarray
            Heatmap array to modify.

        source : tuple of float
            Current value range of the input array, given as (min, max), where both are float values.

        target : tuple of float
            Desired output value range of the array, given as (min, max), where both are float values.

        Returns
        -------
        arr_target : ndarray
            Input array, with value range projected to the desired target value range.

        """
        ia.do_assert(ia.is_np_array(arr))

        if isinstance(source, HeatmapsOnImage):
            source = (source.min_value, source.max_value)
        else:
            ia.do_assert(isinstance(source, tuple))
            ia.do_assert(len(source) == 2)
            ia.do_assert(source[0] < source[1])

        if isinstance(target, HeatmapsOnImage):
            target = (target.min_value, target.max_value)
        else:
            ia.do_assert(isinstance(target, tuple))
            ia.do_assert(len(target) == 2)
            ia.do_assert(target[0] < target[1])

        # Check if source and target are the same (with a tiny bit of tolerance)
        # if so, evade compuation and just copy the array instead.
        # This is reasonable, as source and target will often both be (0.0, 1.0).
        eps = np.finfo(arr.dtype).eps
        mins_same = source[0] - 10*eps < target[0] < source[0] + 10*eps
        maxs_same = source[1] - 10*eps < target[1] < source[1] + 10*eps
        if mins_same and maxs_same:
            return np.copy(arr)

        min_source, max_source = source
        min_target, max_target = target

        diff_source = max_source - min_source
        diff_target = max_target - min_target

        arr_0to1 = (arr - min_source) / diff_source
        arr_target = min_target + arr_0to1 * diff_target

        return arr_target