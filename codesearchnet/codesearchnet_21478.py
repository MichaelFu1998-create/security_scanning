def siblings(self, name=None):
        """
        Yields all siblings of this node (not including the node itself).

        :param name: If specified, only consider elements with this tag name
        """
        if self.parent and self.index:
            for c in self.parent._children:
                if c.index != self.index and (name is None or name == c.tagname):
                    yield c