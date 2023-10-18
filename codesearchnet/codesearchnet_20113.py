def add(self, *entries):
        """
        Add a source, either specified by glottolog reference id, or as bibtex record.
        """
        for entry in entries:
            if isinstance(entry, string_types):
                self._add_entries(database.parse_string(entry, bib_format='bibtex'))
            else:
                self._add_entries(entry)