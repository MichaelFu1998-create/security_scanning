def update_keywords(self):
        """653 Free Keywords."""
        for field in record_get_field_instances(self.record, '653', ind1='1'):
            subs = field_get_subfields(field)
            new_subs = []
            if 'a' in subs:
                for val in subs['a']:
                    new_subs.extend([('9', 'author'), ('a', val)])
            new_field = create_field(subfields=new_subs, ind1='1')
            record_replace_field(
                self.record, '653', new_field, field_position_global=field[4])