def get_xml(self):
        """Return the XML stanza representation.

        This returns the original or cached XML representation, which
        may be much more efficient than `as_xml`.

        Result of this function should never be modified.

        :returntype: :etree:`ElementTree.Element`"""
        if not self._dirty:
            return self._element
        element = self.as_xml()
        self._element = element
        self._dirty = False
        return element