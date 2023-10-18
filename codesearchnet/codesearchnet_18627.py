def update_cnum(self):
        """Check if we shall add cnum in 035."""
        if "ConferencePaper" not in self.collections:
            cnums = record_get_field_values(self.record, '773', code="w")
            for cnum in cnums:
                cnum_subs = [
                    ("9", "INSPIRE-CNUM"),
                    ("a", cnum)
                ]
                record_add_field(self.record, "035", subfields=cnum_subs)