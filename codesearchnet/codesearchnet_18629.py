def update_system_numbers(self):
        """035 Externals."""
        scn_035_fields = record_get_field_instances(self.record, '035')
        new_fields = []
        for field in scn_035_fields:
            subs = field_get_subfields(field)
            if '9' in subs:
                if subs['9'][0].lower() == "cds" and subs.get('a'):
                    self.add_control_number("001", subs.get('a')[0])
                if subs['9'][0].lower() in ["inspire", "spirestex", "inspiretex", "desy", "cds"]:
                    continue
            new_fields.append(field_get_subfield_instances(field))
        record_delete_fields(self.record, tag="035")
        for field in new_fields:
            record_add_field(self.record, tag="035", subfields=field)