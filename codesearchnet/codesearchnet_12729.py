def _check_peptide_inputs(self, peptides):
        """
        Check peptide sequences to make sure they are valid for this predictor.
        """
        require_iterable_of(peptides, string_types)
        check_X = not self.allow_X_in_peptides
        check_lower = not self.allow_lowercase_in_peptides
        check_min_length = self.min_peptide_length is not None
        min_length = self.min_peptide_length
        check_max_length = self.max_peptide_length is not None
        max_length = self.max_peptide_length
        for p in peptides:
            if not p.isalpha():
                raise ValueError("Invalid characters in peptide '%s'" % p)
            elif check_X and "X" in p:
                raise ValueError("Invalid character 'X' in peptide '%s'" % p)
            elif check_lower and not p.isupper():
                raise ValueError("Invalid lowercase letters in peptide '%s'" % p)
            elif check_min_length and len(p) < min_length:
                raise ValueError(
                    "Peptide '%s' too short (%d chars), must be at least %d" % (
                        p, len(p), min_length))
            elif check_max_length and len(p) > max_length:
                raise ValueError(
                    "Peptide '%s' too long (%d chars), must be at least %d" % (
                        p, len(p), max_length))