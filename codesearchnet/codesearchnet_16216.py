def format_map(self, format_string, mapping):
        """format a string by a map

        Args:
            format_string(str): A format string
            mapping(dict): A map to format the string

        Returns:
            A formatted string.

        Raises:
            KeyError: if key is not provided by the given map.
        """
        return self.vformat(format_string, args=None, kwargs=mapping)