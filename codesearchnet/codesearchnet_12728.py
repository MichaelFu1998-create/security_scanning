def _check_peptide_lengths(self, peptide_lengths=None):
        """
        If peptide lengths not specified, then try using the default
        lengths associated with this predictor object. If those aren't
        a valid non-empty sequence of integers, then raise an exception.
        Otherwise return the peptide lengths.
        """
        if not peptide_lengths:
            peptide_lengths = self.default_peptide_lengths

        if not peptide_lengths:
            raise ValueError(
                ("Must either provide 'peptide_lengths' argument "
                "or set 'default_peptide_lengths"))
        if isinstance(peptide_lengths, int):
            peptide_lengths = [peptide_lengths]
        require_iterable_of(peptide_lengths, int)
        for peptide_length in peptide_lengths:
            if (self.min_peptide_length is not None and
                    peptide_length < self.min_peptide_length):
                raise ValueError(
                    "Invalid peptide length %d, shorter than min %d" % (
                        peptide_length,
                        self.min_peptide_length))
            elif (self.max_peptide_length is not None and
                    peptide_length > self.max_peptide_length):
                raise ValueError(
                    "Invalid peptide length %d, longer than max %d" % (
                        peptide_length,
                        self.max_peptide_length))
        return peptide_lengths