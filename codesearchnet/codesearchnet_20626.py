def unmask(self, arr):
        """Use self.mask to reshape arr and self.img to get an affine and header to create
        a new self.img using the data in arr.
        If self.has_mask() is False, will return the same arr.
        """
        self._check_for_mask()

        if 1 > arr.ndim > 2:
            raise ValueError('The given array has {} dimensions while my mask has {}. '
                             'Masked data must be 1D or 2D array. '.format(arr.ndim,
                                                                           len(self.mask.shape)))

        if arr.ndim == 2:
            return matrix_to_4dvolume(arr, self.mask.get_data())
        elif arr.ndim == 1:
            return vector_to_volume(arr, self.mask.get_data())