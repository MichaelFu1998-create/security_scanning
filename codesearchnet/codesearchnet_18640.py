def update_thesis_information(self):
        """501 degree info - move subfields."""
        fields_501 = record_get_field_instances(self.record, '502')
        for field in fields_501:
            new_subs = []
            for key, value in field[0]:
                if key == 'b':
                    new_subs.append(('a', value))
                elif key == 'c':
                    new_subs.append(('b', value))
                elif key == 'd':
                    new_subs.append(('c', value))
                else:
                    new_subs.append((key, value))
            record_delete_field(self.record, tag="502",
                                field_position_global=field[4])
            record_add_field(self.record, "502", subfields=new_subs)