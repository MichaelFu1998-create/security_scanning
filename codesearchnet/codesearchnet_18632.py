def update_title_to_proceeding(self):
        """Move title info from 245 to 111 proceeding style."""
        titles = record_get_field_instances(self.record,
                                            tag="245")
        for title in titles:
            subs = field_get_subfields(title)
            new_subs = []
            if "a" in subs:
                new_subs.append(("a", subs['a'][0]))
            if "b" in subs:
                new_subs.append(("c", subs['b'][0]))
            record_add_field(self.record,
                             tag="111",
                             subfields=new_subs)
        record_delete_fields(self.record, tag="245")
        record_delete_fields(self.record, tag="246")