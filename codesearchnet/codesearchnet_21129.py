def _parse_allele_data(self):
        """Create list of Alleles from VCF line data"""
        return [Allele(sequence=x) for x in
                [self.ref_allele] + self.alt_alleles]