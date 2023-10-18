def col(self, c):
        """Parse colour specification"""
        m = self.COLOUR.search(c)
        if not m:
            self.logger.fatal("Cannot parse colour specification %r.", c)
            raise ParseError("XPM reader: Cannot parse colour specification {0!r}.".format(c))
        value = m.group('value')
        color = m.group('symbol')
        self.logger.debug("%s: %s %s\n", c.strip(), color, value)
        return color, value