def update_isbn(self):
        """Remove dashes from ISBN."""
        isbns = record_get_field_instances(self.record, '020')
        for field in isbns:
            for idx, (key, value) in enumerate(field[0]):
                if key == 'a':
                    field[0][idx] = ('a', value.replace("-", "").strip())