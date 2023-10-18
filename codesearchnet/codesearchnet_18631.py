def update_notes(self):
        """Remove INSPIRE specific notes."""
        fields = record_get_field_instances(self.record, '500')
        for field in fields:
            subs = field_get_subfields(field)
            for sub in subs.get('a', []):
                sub = sub.strip()  # remove any spaces before/after
                if sub.startswith("*") and sub.endswith("*"):
                    record_delete_field(self.record, tag="500",
                                        field_position_global=field[4])