def multiply(self, multiplier, axis=None):
        """
        In-place multiplication

        :param multiplier: A matrix or vector to be multiplied
        :param axis: The dim along which 'multiplier' is multiplied
        :return: Nothing (as it performs in-place operations)
        """
        if self.finalized:
            if multiplier.ndim == 1:
                if axis == 0:  # multiplier is np.array of length |haplotypes|
                    raise NotImplementedError('The method is not yet implemented for the axis.')
                elif axis == 1:  # multiplier is np.array of length |loci|
                    sz = len(multiplier)
                    multiplier_mat = lil_matrix((sz, sz))
                    multiplier_mat.setdiag(multiplier)
                    for hid in xrange(self.shape[1]):
                        self.data[hid] = self.data[hid] * multiplier_mat
                elif axis == 2:  # multiplier is np.array of length |reads|
                    for hid in xrange(self.shape[1]):
                        self.data[hid].data *= multiplier[self.data[hid].indices]
                else:
                    raise RuntimeError('The axis should be 0, 1, or 2.')
            elif multiplier.ndim == 2:
                if axis == 0:  # multiplier is sp.sparse matrix of shape |reads| x |haplotypes|
                    for hid in xrange(self.shape[1]):
                        self.data[hid].data *= multiplier[self.data[hid].indices, hid]
                elif axis == 1:  # multiplier is sp.sparse matrix of shape |reads| x |loci|
                    for hid in xrange(self.shape[1]):
                        self.data[hid] = self.data[hid].multiply(multiplier)
                elif axis == 2:  # multiplier is np.matrix of shape |haplotypes| x |loci|
                    for hid in xrange(self.shape[1]):
                        multiplier_vec = multiplier[hid, :]
                        multiplier_vec = multiplier_vec.ravel()
                        self.data[hid].data *= multiplier_vec.repeat(np.diff(self.data[hid].indptr))
                else:
                    raise RuntimeError('The axis should be 0, 1, or 2.')
            elif isinstance(multiplier, Sparse3DMatrix):  # multiplier is Sparse3DMatrix object
                    for hid in xrange(self.shape[1]):
                        self.data[hid] = self.data[hid].multiply(multiplier.data[hid])
            else:
                raise RuntimeError('The multiplier should be 1, 2 dimensional numpy array or a Sparse3DMatrix object.')
        else:
            raise RuntimeError('The original matrix must be finalized.')