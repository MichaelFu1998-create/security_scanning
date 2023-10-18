def keep_only_fields(self):
        """Keep only fields listed in field_list."""
        for tag in self.record.keys():
            if tag not in self.fields_list:
                record_delete_fields(self.record, tag)