def children(self, name=None, reverse=False):
        """
        A generator yielding children of this node.

        :param name: If specified, only consider elements with this tag name
        :param reverse: If ``True``, children will be yielded in reverse declaration order
        """
        elems = self._children
        if reverse:
            elems = reversed(elems)
        for elem in elems:
            if name is None or elem.tagname == name:
                yield elem