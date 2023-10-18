def strip_fields(self):
        """Clear any fields listed in field_list."""
        for tag in self.record.keys():
            if tag in self.fields_list:
                record_delete_fields(self.record, tag)