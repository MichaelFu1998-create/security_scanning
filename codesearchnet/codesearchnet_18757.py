def update_pagenumber(self):
        """300 page number."""
        for field in record_get_field_instances(self.record, '300'):
            for idx, (key, value) in enumerate(field[0]):
                if key == 'a':
                    if "mult." not in value and value != " p":
                        field[0][idx] = ('a', re.sub(r'[^\d-]+', '', value))
                    else:
                        record_delete_field(self.record, '300',
                                            field_position_global=field[4])
                        break