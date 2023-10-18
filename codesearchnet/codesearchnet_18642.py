def update_date(self):
        """269 Date normalization."""
        dates_269 = record_get_field_instances(self.record, '269')
        for idx, field in enumerate(dates_269):
            new_subs = []
            old_subs = field[0]
            for code, value in old_subs:
                if code == "c":
                    new_subs.append((
                        "c",
                        convert_date_from_iso_to_human(value)
                    ))
                else:
                    new_subs.append((code, value))
            dates_269[idx] = field_swap_subfields(field, new_subs)