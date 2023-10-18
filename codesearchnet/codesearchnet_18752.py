def is_published(self):
        """Check fields 980 and 773 to see if the record has already been published.

        :return: True is published, else False
        """
        field980 = record_get_field_instances(self.record, '980')
        field773 = record_get_field_instances(self.record, '773')
        for f980 in field980:
            if 'a' in field_get_subfields(f980):
                for f773 in field773:
                    if 'p' in field_get_subfields(f773):
                        return True
        return False