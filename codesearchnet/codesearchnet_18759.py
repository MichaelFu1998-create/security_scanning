def update_thesis_supervisors(self):
        """700 -> 701 Thesis supervisors."""
        for field in record_get_field_instances(self.record, '700'):
            record_add_field(self.record, '701', subfields=field[0])
        record_delete_fields(self.record, '700')