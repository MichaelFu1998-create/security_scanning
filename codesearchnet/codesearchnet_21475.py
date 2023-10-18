def iter(self, name=None):
        """
        Recursively find any descendants of this node with the given tag name. If a tag name is omitted, this will
        yield every descendant node.

        :param name: If specified, only consider elements with this tag name
        :returns: A generator yielding descendants of this node
        """
        for c in self._children:
            if name is None or c.tagname == name:
                yield c
            for gc in c.find(name):
                yield gc