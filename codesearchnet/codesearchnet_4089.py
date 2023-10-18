def append(self, linenumber, raw_text, cells):
        """Add another row of data from a test suite"""
        self.rows.append(Row(linenumber, raw_text, cells))