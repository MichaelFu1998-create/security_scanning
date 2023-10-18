def update_system_numbers(self):
        """035 Externals."""
        scn_035_fields = record_get_field_instances(self.record, '035')
        forbidden_values = ["cercer",
                            "inspire",
                            "xx",
                            "cern annual report",
                            "cmscms",
                            "wai01"]
        for field in scn_035_fields:
            subs = field_get_subfields(field)
            if '9' in subs:
                if 'a' not in subs:
                    continue
                for sub in subs['9']:
                    if sub.lower() in forbidden_values:
                        break
                else:
                    # No forbidden values (We did not "break")
                    suffixes = [s.lower() for s in subs['9']]
                    if 'spires' in suffixes:
                        new_subs = [('a', 'SPIRES-%s' % subs['a'][0])]
                        record_add_field(
                            self.record, '970', subfields=new_subs)
                        continue
            if 'a' in subs:
                for sub in subs['a']:
                    if sub.lower() in forbidden_values:
                        record_delete_field(self.record, tag="035",
                                            field_position_global=field[4])