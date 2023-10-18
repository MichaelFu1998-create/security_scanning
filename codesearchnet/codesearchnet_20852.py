def get_ISSNs(self):
        """
        Get list of VALID ISSNs (``022a``).

        Returns:
            list: List with *valid* ISSN strings.
        """
        invalid_issns = set(self.get_invalid_ISSNs())

        return [
            self._clean_isbn(issn)
            for issn in self["022a"]
            if self._clean_isbn(issn) not in invalid_issns
        ]