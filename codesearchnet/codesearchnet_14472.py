def find_match(self):
        """Try to find a pattern that matches the source and calll a parser
        method to create Python objects.

        A callback that raises an IgnoredMatchException indicates that the
        given string data is ignored by the parser and no objects are created.

        If none of the pattern match a NoMatchException is raised.
        """
        for pattern, callback in self.rules:
            match = pattern.match(self.source, pos=self.pos)

            if not match:
                continue

            try:
                node = callback(match)
            except IgnoredMatchException:
                pass
            else:
                self.seen.append(node)

            return match

        raise NoMatchException(
            'None of the known patterns match for {}'
            ''.format(self.source[self.pos:])
        )