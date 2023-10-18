def update_subject_categories(self, primary, secondary, kb):
        """650 Translate Categories."""
        category_fields = record_get_field_instances(self.record,
                                                     tag='650',
                                                     ind1='1',
                                                     ind2='7')
        record_delete_fields(self.record, "650")
        for field in category_fields:
            for idx, (key, value) in enumerate(field[0]):
                if key == 'a':
                    new_value = self.get_config_item(value, kb)
                    if new_value != value:
                        new_subs = [('2', secondary), ('a', new_value)]
                    else:
                        new_subs = [('2', primary), ('a', value)]
                    record_add_field(self.record, "650", ind1="1", ind2="7",
                                     subfields=new_subs)
                    break