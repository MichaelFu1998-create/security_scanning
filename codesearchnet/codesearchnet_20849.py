def get_authors(self):
        """
        Returns:
            list: Authors represented as :class:`.Person` objects.
        """
        authors = self._parse_persons("100", "a")
        authors += self._parse_persons("600", "a")
        authors += self._parse_persons("700", "a")
        authors += self._parse_persons("800", "a")

        return authors