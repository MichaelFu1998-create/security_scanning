def update_probability_at_read_level(self, model=3):
        """
        Updates the probability of read origin at read level

        :param model: Normalization model (1: Gene->Allele->Isoform, 2: Gene->Isoform->Allele, 3: Gene->Isoform*Allele, 4: Gene*Isoform*Allele)
        :return: Nothing (as it performs in-place operations)
        """
        self.probability.reset()  # reset to alignment incidence matrix
        if model == 1:
            self.probability.multiply(self.allelic_expression, axis=APM.Axis.READ)
            self.probability.normalize_reads(axis=APM.Axis.HAPLOGROUP, grouping_mat=self.t2t_mat)
            haplogroup_sum_mat = self.allelic_expression * self.t2t_mat
            self.probability.multiply(haplogroup_sum_mat, axis=APM.Axis.READ)
            self.probability.normalize_reads(axis=APM.Axis.GROUP, grouping_mat=self.t2t_mat)
            self.probability.multiply(haplogroup_sum_mat.sum(axis=0), axis=APM.Axis.HAPLOTYPE)
            self.probability.normalize_reads(axis=APM.Axis.READ)
        elif model == 2:
            self.probability.multiply(self.allelic_expression, axis=APM.Axis.READ)
            self.probability.normalize_reads(axis=APM.Axis.LOCUS)
            self.probability.multiply(self.allelic_expression.sum(axis=0), axis=APM.Axis.HAPLOTYPE)
            self.probability.normalize_reads(axis=APM.Axis.GROUP, grouping_mat=self.t2t_mat)
            self.probability.multiply((self.allelic_expression * self.t2t_mat).sum(axis=0), axis=APM.Axis.HAPLOTYPE)
            self.probability.normalize_reads(axis=APM.Axis.READ)
        elif model == 3:
            self.probability.multiply(self.allelic_expression, axis=APM.Axis.READ)
            self.probability.normalize_reads(axis=APM.Axis.GROUP, grouping_mat=self.t2t_mat)
            self.probability.multiply((self.allelic_expression * self.t2t_mat).sum(axis=0), axis=APM.Axis.HAPLOTYPE)
            self.probability.normalize_reads(axis=APM.Axis.READ)
        elif model == 4:
            self.probability.multiply(self.allelic_expression, axis=APM.Axis.READ)
            self.probability.normalize_reads(axis=APM.Axis.READ)
        else:
            raise RuntimeError('The read normalization model should be 1, 2, 3, or 4.')