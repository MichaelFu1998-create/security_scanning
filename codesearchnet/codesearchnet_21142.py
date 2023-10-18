def as_dict(self, *args, **kwargs):
        """Return ClinVarAllele data as dict object."""
        self_as_dict = super(ClinVarAllele, self).as_dict(*args, **kwargs)
        self_as_dict['hgvs'] = self.hgvs
        self_as_dict['clnalleleid'] = self.clnalleleid
        self_as_dict['clnsig'] = self.clnsig
        self_as_dict['clndn'] = self.clndn
        self_as_dict['clndisdb'] = self.clndisdb
        self_as_dict['clnvi'] = self.clnvi
        return self_as_dict