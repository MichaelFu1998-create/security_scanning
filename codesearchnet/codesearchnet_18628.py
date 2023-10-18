def update_hidden_notes(self):
        """Remove hidden notes and tag a CERN if detected."""
        if not self.tag_as_cern:
            notes = record_get_field_instances(self.record,
                                               tag="595")
            for field in notes:
                for dummy, value in field[0]:
                    if value == "CDS":
                        self.tag_as_cern = True
        record_delete_fields(self.record, tag="595")