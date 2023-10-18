def is_published(self):
        """Check fields 980 and 773 to see if the record has already been published.

        :return: True is published, else False
        """
        field773 = record_get_field_instances(self.record, '773')
        for f773 in field773:
            if 'c' in field_get_subfields(f773):
                return True
        return False