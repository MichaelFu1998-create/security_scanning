def normalize_reads(self, axis, grouping_mat=None):
        """
        Read-wise normalization

        :param axis: The dimension along which we want to normalize values
        :param grouping_mat: An incidence matrix that specifies which isoforms are from a same gene
        :return: Nothing (as the method performs in-place operations)
        :rtype: None
        """
        if self.finalized:
            if axis == self.Axis.LOCUS:  # Locus-wise normalization on each read
                normalizer = self.sum(axis=self.Axis.HAPLOTYPE)  # Sparse matrix of |reads| x |loci|
                normalizer.eliminate_zeros()
                for hid in xrange(self.num_haplotypes):
                    self.data[hid].eliminate_zeros()  # Trying to avoid numerical problem (inf or nan)
                    self.data[hid] = np.divide(self.data[hid], normalizer)  # element-wise division
            elif axis == self.Axis.HAPLOTYPE:  # haplotype-wise normalization on each read
                for hid in xrange(self.num_haplotypes):
                    normalizer = self.data[hid].sum(axis=self.Axis.HAPLOTYPE)  # 1-dim Sparse matrix of |reads| x 1
                    normalizer = normalizer.A.flatten()
                    self.data[hid].data /= normalizer[self.data[hid].indices]
            elif axis == self.Axis.READ:  # normalization each read as a whole
                sum_mat = self.sum(axis=self.Axis.LOCUS)
                normalizer = sum_mat.sum(axis=self.Axis.HAPLOTYPE)
                normalizer = normalizer.ravel()
                for hid in xrange(self.num_haplotypes):
                    self.data[hid].data /= normalizer[self.data[hid].indices]
            elif axis == self.Axis.GROUP:  # group-wise normalization on each read
                if grouping_mat is None:
                    raise RuntimeError('Group information matrix is missing.')
                normalizer = self.sum(axis=self.Axis.HAPLOTYPE) * grouping_mat
                for hid in xrange(self.num_haplotypes):
                    self.data[hid].eliminate_zeros()  # Trying to avoid numerical problem (inf or nan)
                    self.data[hid] = np.divide(self.data[hid], normalizer)
            elif axis == self.Axis.HAPLOGROUP:  # haplotype-wise & group-wise normalization on each read
                if grouping_mat is None:
                    raise RuntimeError('Group information matrix is missing.')
                for hid in xrange(self.num_haplotypes):  # normalizer is different hap-by-hap
                    normalizer = self.data[hid] * grouping_mat  # Sparse matrix of |reads| x |loci|
                    self.data[hid].eliminate_zeros()  # Trying to avoid numerical problem (inf or nan)
                    self.data[hid] = np.divide(self.data[hid], normalizer)
            else:
                raise RuntimeError('The axis should be 0, 1, 2, or 3.')
        else:
            raise RuntimeError('The original matrix must be finalized.')