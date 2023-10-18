def update_collections(self):
        """Try to determine which collections this record should belong to."""
        for value in record_get_field_values(self.record, '980', code='a'):
            if 'NOTE' in value.upper():
                self.collections.add('NOTE')
            if 'THESIS' in value.upper():
                self.collections.add('THESIS')

            if 'PUBLISHED' in value.upper():
                self.collections.add('ARTICLE')

            if 'CONFERENCES' in value.upper():
                self.collections.add('ANNOUNCEMENT')

            if 'PROCEEDINGS' in value.upper():
                self.collections.add('PROCEEDINGS')
            elif 'CONFERENCEPAPER' in value.upper() and \
                 "ConferencePaper" not in self.collections:
                self.collections.add('ConferencePaper')
                if self.is_published() and "ARTICLE" not in self.collections:
                    self.collections.add('ARTICLE')
                else:
                    self.collections.add('PREPRINT')

            if "HIDDEN" in value.upper():
                self.hidden = True

        # Clear out any existing ones.
        record_delete_fields(self.record, "980")

        if not self.collections:
            self.collections.add('PREPRINT')

        for collection in self.collections:
            record_add_field(self.record,
                             tag='980',
                             subfields=[('a', collection)])
            if collection in self.collection_base:
                subs = [('a', self.collection_base[collection])]
                record_add_field(self.record,
                                 tag='960',
                                 subfields=subs)