def last(self, name=None):
        """
        Returns the last child of this node.

        :param name: If specified, only consider elements with this tag name
        :rtype: :class:`XmlElement`
        """
        for c in self.children(name, reverse=True):
            return c