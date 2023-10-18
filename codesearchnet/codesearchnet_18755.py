def update_reportnumbers(self):
        """Handle reportnumbers. """
        rep_088_fields = record_get_field_instances(self.record, '088')
        for field in rep_088_fields:
            subs = field_get_subfields(field)
            if '9' in subs:
                for val in subs['9']:
                    if val.startswith('P0') or val.startswith('CM-P0'):
                        sf = [('9', 'CERN'), ('b', val)]
                        record_add_field(self.record, '595', subfields=sf)
            for key, val in field[0]:
                if key in ['a', '9'] and not val.startswith('SIS-'):
                    record_add_field(
                        self.record, '037', subfields=[('a', val)])
        record_delete_fields(self.record, "088")

        # 037 Externals also...
        rep_037_fields = record_get_field_instances(self.record, '037')
        for field in rep_037_fields:
            subs = field_get_subfields(field)
            if 'a' in subs:
                for value in subs['a']:
                    if 'arXiv' in value:
                        new_subs = [('a', value), ('9', 'arXiv')]
                        for fld in record_get_field_instances(self.record,  '695'):
                            for key, val in field_get_subfield_instances(fld):
                                if key == 'a':
                                    new_subs.append(('c', val))
                                    break
                        nf = create_field(subfields=new_subs)
                        record_replace_field(self.record, '037', nf, field[4])
            for key, val in field[0]:
                if key in ['a', '9'] and val.startswith('SIS-'):
                    record_delete_field(
                        self.record, '037', field_position_global=field[4])