def parse(self, text, key=None):
        """ Parses a response.

        Args:
            text (str): Text to parse

        Kwargs:
            key (str): Key to look for, if any

        Returns:
            Parsed value

        Raises:
            ValueError
        """
        try:
            data = json.loads(text)
        except ValueError as e:
            raise ValueError("%s: Value: [%s]" % (e, text))

        if data and key:
            if key not in data:
                raise ValueError("Invalid response (key %s not found): %s" % (key, data))
            data = data[key]
        return data