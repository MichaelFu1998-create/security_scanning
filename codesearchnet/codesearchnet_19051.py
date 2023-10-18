def pull_alignments_from(self, reads_to_use, shallow=False):
        """
        Pull out alignments of certain reads

        :param reads_to_use: numpy array of dtype=bool specifying which reads to use
        :param shallow: whether to copy sparse 3D matrix only or not
        :return: a new AlignmentPropertyMatrix object that particular reads are
        """
        new_alnmat = self.copy(shallow=shallow)
        for hid in xrange(self.num_haplotypes):
            hdata = new_alnmat.data[hid]
            hdata.data *= reads_to_use[hdata.indices]
            hdata.eliminate_zeros()
        if new_alnmat.count is not None:
            new_alnmat.count[np.logical_not(reads_to_use)] = 0
        return new_alnmat