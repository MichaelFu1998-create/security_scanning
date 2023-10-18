def determine_collections(self):
        """Try to determine which collections this record should belong to."""
        for value in record_get_field_values(self.record, '980', code='a'):
            if 'NOTE' in value.upper():
                self.collections.add('NOTE')
            if 'THESIS' in value.upper():
                self.collections.add('THESIS')
            if 'CONFERENCEPAPER' in value.upper():
                self.collections.add('ConferencePaper')
            if "HIDDEN" in value.upper():
                self.hidden = True

        if self.is_published():
            self.collections.add("PUBLISHED")
            self.collections.add("CITEABLE")

        if 'NOTE' not in self.collections:
            from itertools import product
            # TODO: Move this to a KB
            kb = ['ATLAS-CONF-', 'CMS-PAS-', 'ATL-', 'CMS-DP-',
                  'ALICE-INT-', 'LHCb-PUB-']
            values = record_get_field_values(self.record, "088", code='a')
            for val, rep in product(values, kb):
                if val.startswith(rep):
                    self.collections.add('NOTE')
                    break

        # 980 Arxiv tag
        if record_get_field_values(self.record, '035',
                                   filter_subfield_code="a",
                                   filter_subfield_value="arXiv"):
            self.collections.add("arXiv")

        # 980 HEP && CORE
        self.collections.add('HEP')
        self.collections.add('CORE')

        # 980 Conference Note
        if 'ConferencePaper' not in self.collections:
            for value in record_get_field_values(self.record,
                                                 tag='962',
                                                 code='n'):
                if value[-2:].isdigit():
                    self.collections.add('ConferencePaper')
                    break
        # Clear out any existing ones.
        record_delete_fields(self.record, "980")