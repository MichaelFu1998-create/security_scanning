def reset(self, pseudocount=0.0):
        """
        Initializes the probability of read origin according to the alignment profile

        :param pseudocount: Uniform prior for allele specificity estimation
        :return: Nothing (as it performs an in-place operations)
        """
        self.probability.reset()
        self.probability.normalize_reads(axis=APM.Axis.READ)  # Initialize alignment probability matrix
        self.allelic_expression = self.probability.sum(axis=APM.Axis.READ)
        if self.target_lengths is not None:  # allelic_expression will be at depth-level
            self.allelic_expression = np.divide(self.allelic_expression, self.target_lengths)
        if pseudocount > 0.0:  # pseudocount is at depth-level
            orig_allelic_expression_sum = self.allelic_expression.sum()
            nzloci = np.nonzero(self.allelic_expression)[1]
            self.allelic_expression[:, nzloci] += pseudocount
            self.allelic_expression *= (orig_allelic_expression_sum / self.allelic_expression.sum())