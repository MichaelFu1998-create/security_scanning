def _convenienceMatch(self, role, attr, match):
        """Method used by role based convenience functions to find a match"""
        kwargs = {}
        # If the user supplied some text to search for,
        # supply that in the kwargs
        if match:
            kwargs[attr] = match
        return self.findAll(AXRole=role, **kwargs)