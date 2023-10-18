def getheaders(self, name):
        """Get all values for a header.

        This returns a list of values for headers given more than once; each
        value in the result list is stripped in the same way as the result of
        getheader().  If the header is not given, return an empty list.
        """
        result = []
        current = ''
        have_header = 0
        for s in self.getallmatchingheaders(name):
            if s[0].isspace():
                if current:
                    current = "%s\n %s" % (current, s.strip())
                else:
                    current = s.strip()
            else:
                if have_header:
                    result.append(current)
                current = s[s.find(":") + 1:].strip()
                have_header = 1
        if have_header:
            result.append(current)
        return result