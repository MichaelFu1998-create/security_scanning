def isheader(self, line):
        """Determine whether a given line is a legal header.

        This method should return the header name, suitably canonicalized.
        You may override this method in order to use Message parsing on tagged
        data in RFC 2822-like formats with special header formats.
        """
        i = line.find(':')
        if i > -1:
            return line[:i].lower()
        return None