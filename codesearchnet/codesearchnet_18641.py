def update_pagenumber(self):
        """300 page number."""
        pages = record_get_field_instances(self.record, '300')
        for field in pages:
            for idx, (key, value) in enumerate(field[0]):
                if key == 'a':
                    field[0][idx] = ('a', "{0} p".format(value))