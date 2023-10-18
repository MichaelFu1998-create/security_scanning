def _baseattrs(self):
        """A dict of members expressed in literals"""

        result = {
            "type": type(self).__name__,
            "id": id(self),
            "name": self.name,
            "fullname": self.fullname,
            "repr": self._get_repr(),
        }

        return result