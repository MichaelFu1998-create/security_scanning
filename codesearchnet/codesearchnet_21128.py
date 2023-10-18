def as_dict(self):
        """Return Allele data as dict object."""
        self_as_dict = dict()
        self_as_dict['sequence'] = self.sequence
        if hasattr(self, 'frequency'):
            self_as_dict['frequency'] = self.frequency
        return self_as_dict