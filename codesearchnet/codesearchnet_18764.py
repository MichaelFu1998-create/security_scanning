def update_journals(self):
        """773 journal translations."""
        for field in record_get_field_instances(self.record, '773'):
            subs = field_get_subfield_instances(field)
            new_subs = []
            for idx, (key, value) in enumerate(subs):
                if key == 'p':
                    journal_name = self.get_config_item(value, "journals", allow_substring=False)
                    journal_name = journal_name.replace('. ', '.').strip()
                    new_subs.append((key, journal_name))
                else:
                    new_subs.append((key, value))
            record_delete_field(self.record, tag="773",
                                field_position_global=field[4])
            record_add_field(self.record, "773", subfields=new_subs)