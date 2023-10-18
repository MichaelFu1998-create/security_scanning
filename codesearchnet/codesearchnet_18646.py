def update_languages(self):
        """041 Language."""
        language_fields = record_get_field_instances(self.record, '041')
        language = "eng"
        record_delete_fields(self.record, "041")
        for field in language_fields:
            subs = field_get_subfields(field)
            if 'a' in subs:
                language = self.get_config_item(subs['a'][0], "languages")
                break
        new_subs = [('a', language)]
        record_add_field(self.record, "041", subfields=new_subs)