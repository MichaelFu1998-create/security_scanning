def get_ISBNs(self):
        """
        Get list of VALID ISBN.

        Returns:
            list: List with *valid* ISBN strings.
        """
        invalid_isbns = set(self.get_invalid_ISBNs())

        valid_isbns = [
            self._clean_isbn(isbn)
            for isbn in self["020a"]
            if self._clean_isbn(isbn) not in invalid_isbns
        ]

        if valid_isbns:
            return valid_isbns

        # this is used sometimes in czech national library
        return [
            self._clean_isbn(isbn)
            for isbn in self["901i"]
        ]