def update_reportnumbers(self):
        """Update reportnumbers."""
        report_037_fields = record_get_field_instances(self.record, '037')
        for field in report_037_fields:
            subs = field_get_subfields(field)
            for val in subs.get("a", []):
                if "arXiv" not in val:
                    record_delete_field(self.record,
                                        tag="037",
                                        field_position_global=field[4])
                    new_subs = [(code, val[0]) for code, val in subs.items()]
                    record_add_field(self.record, "088", subfields=new_subs)
                    break