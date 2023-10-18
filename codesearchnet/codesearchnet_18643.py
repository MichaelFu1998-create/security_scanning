def update_date_year(self):
        """260 Date normalization."""
        dates = record_get_field_instances(self.record, '260')
        for field in dates:
            for idx, (key, value) in enumerate(field[0]):
                if key == 'c':
                    field[0][idx] = ('c', value[:4])
                elif key == 't':
                    del field[0][idx]
        if not dates:
            published_years = record_get_field_values(self.record, "773", code="y")
            if published_years:
                record_add_field(
                    self.record, "260", subfields=[("c", published_years[0][:4])])
            else:
                other_years = record_get_field_values(self.record, "269", code="c")
                if other_years:
                    record_add_field(
                        self.record, "260", subfields=[("c", other_years[0][:4])])