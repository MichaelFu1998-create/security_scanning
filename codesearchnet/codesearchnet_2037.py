def groupdict(self, default=None):
        """Return a dictionary containing all the named subgroups of the match.
        The default argument is used for groups that did not participate in the
        match (defaults to None)."""
        groupdict = {}
        for key, value in self.re.groupindex.items():
            groupdict[key] = self._get_slice(value, default)
        return groupdict