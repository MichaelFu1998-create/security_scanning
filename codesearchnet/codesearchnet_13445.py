def _decode_validity(self, validity):
        """Load data from a ASN.1 validity value.
        """
        not_after = validity.getComponentByName('notAfter')
        not_after = str(not_after.getComponent())
        if isinstance(not_after, GeneralizedTime):
            self.not_after = datetime.strptime(not_after, "%Y%m%d%H%M%SZ")
        else:
            self.not_after = datetime.strptime(not_after, "%y%m%d%H%M%SZ")
        self.alt_names = defaultdict(list)