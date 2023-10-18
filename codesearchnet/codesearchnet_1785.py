def getheader(self, name, default=None):
        """Get the header value for a name.

        This is the normal interface: it returns a stripped version of the
        header value for a given header name, or None if it doesn't exist.
        This uses the dictionary version which finds the *last* such header.
        """
        return self.dict.get(name.lower(), default)