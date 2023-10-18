def _default_value_only(self):
        """
        Return only the default value, if there is one.

        """
        line = self.source[self.col_offset:]
        regex = re.compile('''pyconfig\.[eginst]+\(['"][^)]+?['"], ?(.*?)\)''')
        match = regex.match(line)
        if not match:
            return ''

        return match.group(1)