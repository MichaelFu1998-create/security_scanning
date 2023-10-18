def get_unique_reads(self, ignore_haplotype=False, shallow=False):
        """
        Pull out alignments of uniquely-aligning reads

        :param ignore_haplotype: whether to regard allelic multiread as uniquely-aligning read
        :param shallow: whether to copy sparse 3D matrix only or not
        :return: a new AlignmentPropertyMatrix object that particular reads are
        """
        if self.finalized:
            if ignore_haplotype:
                summat = self.sum(axis=self.Axis.HAPLOTYPE)
                nnz_per_read = np.diff(summat.tocsr().indptr)
                unique_reads = np.logical_and(nnz_per_read > 0, nnz_per_read < 2)
            else:  # allelic multireads should be removed
                alncnt_per_read = self.sum(axis=self.Axis.LOCUS).sum(axis=self.Axis.HAPLOTYPE)
                unique_reads = np.logical_and(alncnt_per_read > 0, alncnt_per_read < 2)
            return self.pull_alignments_from(unique_reads, shallow=shallow)
        else:
            raise RuntimeError('The matrix is not finalized.')