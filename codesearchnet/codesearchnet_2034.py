def finditer(self, string, pos=0, endpos=sys.maxint):
        """Return a list of all non-overlapping matches of pattern in string."""
        scanner = self.scanner(string, pos, endpos)
        return iter(scanner.search, None)