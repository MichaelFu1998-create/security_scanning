def parents(self, name=None):
        """
        Yields all parents of this element, back to the root element.

        :param name: If specified, only consider elements with this tag name
        """
        p = self.parent
        while p is not None:
            if name is None or p.tagname == name:
                yield p
            p = p.parent