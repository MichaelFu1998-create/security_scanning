def getrawheader(self, name):
        """A higher-level interface to getfirstmatchingheader().

        Return a string containing the literal text of the header but with the
        keyword stripped.  All leading, trailing and embedded whitespace is
        kept in the string, however.  Return None if the header does not
        occur.
        """

        lst = self.getfirstmatchingheader(name)
        if not lst:
            return None
        lst[0] = lst[0][len(name) + 1:]
        return ''.join(lst)