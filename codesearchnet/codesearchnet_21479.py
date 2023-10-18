def next(self, name=None):
        """
        Returns the next sibling of this node.

        :param name: If specified, only consider elements with this tag name
        :rtype: :class:`XmlElement`
        """
        if self.parent is None or self.index is None:
            return None
        for idx in xrange(self.index + 1, len(self.parent)):
            if name is None or self.parent[idx].tagname == name:
                return self.parent[idx]