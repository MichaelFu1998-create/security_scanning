def prev(self, name=None):
        """
        Returns the previous sibling of this node.

        :param name: If specified, only consider elements with this tag name
        :rtype: :class:`XmlElement`
        """
        if self.parent is None or self.index is None:
            return None
        for idx in xrange(self.index - 1, -1, -1):
            if name is None or self.parent[idx].tagname == name:
                return self.parent[idx]