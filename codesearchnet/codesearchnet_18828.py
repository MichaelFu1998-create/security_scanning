def _attach_fulltext(self, rec, doi):
        """Attach fulltext FFT."""
        url = os.path.join(self.url_prefix, doi)
        record_add_field(rec, 'FFT',
                         subfields=[('a', url),
                                    ('t', 'INSPIRE-PUBLIC'),
                                    ('d', 'Fulltext')])