def add(self, addend_mat, axis=1):
        """
        In-place addition

        :param addend_mat: A matrix to be added on the Sparse3DMatrix object
        :param axis: The dimension along the addend_mat is added
        :return: Nothing (as it performs in-place operations)
        """
        if self.finalized:
            if axis == 0:
                raise NotImplementedError('The method is not yet implemented for the axis.')
            elif axis == 1:
                for hid in xrange(self.shape[1]):
                    self.data[hid] = self.data[hid] + addend_mat
            elif axis == 2:
                raise NotImplementedError('The method is not yet implemented for the axis.')
            else:
                raise RuntimeError('The axis should be 0, 1, or 2.')
        else:
            raise RuntimeError('The original matrix must be finalized.')