def _valid_distaxis(shapes, ax):
        """`ax` is a valid candidate for a distributed axis if the given
        subarray shapes are all the same when ignoring axis `ax`"""
        compare_shapes = np.vstack(shapes)
        if ax < compare_shapes.shape[1]:
            compare_shapes[:, ax] = -1
        return np.count_nonzero(compare_shapes - compare_shapes[0]) == 0