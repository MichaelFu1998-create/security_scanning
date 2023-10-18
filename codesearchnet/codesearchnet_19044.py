def update_allelic_expression(self, model=3):
        """
        A single EM step: Update probability at read level and then re-estimate allelic specific expression

        :param model: Normalization model (1: Gene->Allele->Isoform, 2: Gene->Isoform->Allele, 3: Gene->Isoform*Allele, 4: Gene*Isoform*Allele)
        :return: Nothing (as it performs in-place operations)
        """
        self.update_probability_at_read_level(model)
        self.allelic_expression = self.probability.sum(axis=APM.Axis.READ)
        if self.target_lengths is not None:
            self.allelic_expression = np.divide(self.allelic_expression, self.target_lengths)