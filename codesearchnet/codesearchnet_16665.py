def _baseattrs(self):
        """A dict of members expressed in literals"""

        result = super()._baseattrs
        result["spaces"] = self.spaces._baseattrs
        return result