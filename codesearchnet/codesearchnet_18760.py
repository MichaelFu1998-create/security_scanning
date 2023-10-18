def update_thesis_information(self):
        """501 degree info - move subfields."""
        fields_501 = record_get_field_instances(self.record, '502')
        for idx, field in enumerate(fields_501):
            new_subs = []
            for key, value in field[0]:
                if key == 'a':
                    new_subs.append(('b', value))
                elif key == 'b':
                    new_subs.append(('c', value))
                elif key == 'c':
                    new_subs.append(('d', value))
                else:
                    new_subs.append((key, value))
            fields_501[idx] = field_swap_subfields(field, new_subs)