def get_key(self):
        """
        Return the call key, even if it has to be parsed from the source.

        """
        if not isinstance(self.key, Unparseable):
            return self.key

        line = self.source[self.col_offset:]
        regex = re.compile('''pyconfig\.[eginst]+\(([^,]+).*?\)''')
        match = regex.match(line)
        if not match:
            return Unparseable()

        return "<%s>" % match.group(1)