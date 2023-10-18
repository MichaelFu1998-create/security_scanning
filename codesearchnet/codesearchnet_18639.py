def update_thesis_supervisors(self):
        """700 -> 701 Thesis supervisors."""
        for field in record_get_field_instances(self.record, '701'):
            subs = list(field[0])
            subs.append(("e", "dir."))
            record_add_field(self.record, '700', subfields=subs)
        record_delete_fields(self.record, '701')