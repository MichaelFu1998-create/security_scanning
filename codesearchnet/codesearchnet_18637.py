def update_dois(self):
        """Remove duplicate BibMatch DOIs."""
        dois = record_get_field_instances(self.record, '024', ind1="7")
        all_dois = {}
        for field in dois:
            subs = field_get_subfield_instances(field)
            subs_dict = dict(subs)
            if subs_dict.get('a'):
                if subs_dict['a'] in all_dois:
                    record_delete_field(self.record, tag='024', ind1='7', field_position_global=field[4])
                    continue
                all_dois[subs_dict['a']] = field