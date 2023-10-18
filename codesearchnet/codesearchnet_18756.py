def update_date(self):
        """269 Date normalization."""
        for field in record_get_field_instances(self.record, '269'):
            for idx, (key, value) in enumerate(field[0]):
                if key == "c":
                    field[0][idx] = ("c", convert_date_to_iso(value))
                    record_delete_fields(self.record, "260")

        if 'THESIS' not in self.collections:
            for field in record_get_field_instances(self.record, '260'):
                record_add_field(self.record, '269', subfields=field[0])
            record_delete_fields(self.record, '260')