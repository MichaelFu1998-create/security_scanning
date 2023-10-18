def prepare(self, pseudocount=0.0, lenfile=None, read_length=100):
        """
        Initializes the probability of read origin according to the alignment profile

        :param pseudocount: Uniform prior for allele specificity estimation
        :return: Nothing (as it performs an in-place operations)
        """
        if self.probability.num_groups > 0:
            self.grp_conv_mat = lil_matrix((self.probability.num_loci, self.probability.num_groups))
            for i in xrange(self.probability.num_groups):
                self.grp_conv_mat[self.probability.groups[i], i] = 1.0
            self.grp_conv_mat = self.grp_conv_mat.tocsc()
            self.t2t_mat = eye(self.probability.num_loci, self.probability.num_loci)
            self.t2t_mat = self.t2t_mat.tolil()
            for tid_list in self.probability.groups:
                for ii in xrange(len(tid_list)):
                    for jj in xrange(ii):
                        i = tid_list[ii]
                        j = tid_list[jj]
                        self.t2t_mat[i, j] = 1
                        self.t2t_mat[j, i] = 1
            self.t2t_mat = self.t2t_mat.tocsc()
        if lenfile is not None:
            hid = dict(zip(self.probability.hname, np.arange(len(self.probability.hname))))
            self.target_lengths = np.zeros((self.probability.num_loci, self.probability.num_haplotypes))
            if self.probability.num_haplotypes > 1:
                with open(lenfile) as fh:
                    for curline in fh:
                        item = curline.rstrip().split("\t")
                        locus, hap = item[0].split("_")
                        self.target_lengths[self.probability.lid[locus], hid[hap]] = max(float(item[1]) - read_length + 1.0, 1.0)
            elif self.probability.num_haplotypes > 0:
                with open(lenfile) as fh:
                    for curline in fh:
                        item = curline.rstrip().split("\t")
                        self.target_lengths[self.probability.lid[item[0]], 0] = max(float(item[1]) - read_length + 1.0, 1.0)
            else:
                raise RuntimeError('There is something wrong with your emase-format alignment file.')
            self.target_lengths = self.target_lengths.transpose()
            #self.target_lengths = self.target_lengths.transpose() / read_length  # lengths in terms of read counts
            if not np.all(self.target_lengths > 0.0):
                raise RuntimeError('There exist transcripts missing length information.')
        self.probability.normalize_reads(axis=APM.Axis.READ)  # Initialize alignment probability matrix
        self.allelic_expression = self.probability.sum(axis=APM.Axis.READ)
        if self.target_lengths is not None:  # allelic_expression will be at depth-level
            self.allelic_expression = np.divide(self.allelic_expression, self.target_lengths)
        if pseudocount > 0.0:  # pseudocount is at depth-level
            orig_allelic_expression_sum = self.allelic_expression.sum()
            nzloci = np.nonzero(self.allelic_expression)[1]
            self.allelic_expression[:, nzloci] += pseudocount
            self.allelic_expression *= (orig_allelic_expression_sum / self.allelic_expression.sum())