def update_authors(self):
        """100 & 700 punctuate author names."""
        author_names = record_get_field_instances(self.record, '100')
        author_names.extend(record_get_field_instances(self.record, '700'))
        for field in author_names:
            subs = field_get_subfields(field)
            if 'i' not in subs or 'XX' in subs['i']:
                if 'j' not in subs or 'YY' in subs['j']:
                    for idx, (key, value) in enumerate(field[0]):
                        if key == 'a':
                            field[0][idx] = ('a', punctuate_authorname(value))