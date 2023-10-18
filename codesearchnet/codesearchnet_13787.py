def parse_from_import_statement(self):
        """Parse a 'from x import y' statement.

        The purpose is to find __future__ statements.
        """
        self.log.debug("parsing from/import statement.")
        is_future_import = self._parse_from_import_source()
        self._parse_from_import_names(is_future_import)