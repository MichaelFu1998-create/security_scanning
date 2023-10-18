def as_dict(self):
        """Dict representation of parsed VCF data"""
        self_as_dict = {'chrom': self.chrom,
                        'start': self.start,
                        'ref_allele': self.ref_allele,
                        'alt_alleles': self.alt_alleles,
                        'alleles': [x.as_dict() for x in self.alleles]}
        try:
            self_as_dict['info'] = self.info
        except AttributeError:
            pass
        return self_as_dict