def update_collaboration(self):
        """710 Collaboration."""
        for field in record_get_field_instances(self.record, '710'):
            subs = field_get_subfield_instances(field)
            for idx, (key, value) in enumerate(subs[:]):
                if key == '5':
                    subs.pop(idx)
                elif value.startswith('CERN. Geneva'):
                    subs.pop(idx)
            if len(subs) == 0:
                record_delete_field(self.record,
                                    tag='710',
                                    field_position_global=field[4])