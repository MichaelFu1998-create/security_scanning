def add_systemnumber(self, source, recid=None):
        """Add 035 number from 001 recid with given source."""
        if not recid:
            recid = self.get_recid()
        if not self.hidden and recid:
            record_add_field(
                self.record,
                tag='035',
                subfields=[('9', source), ('a', recid)]
            )