def add_child(self, child):
        """If the given object is an instance of Child add it to self and
        register self as a parent.
        """
        if not isinstance(child, ChildMixin):
            raise TypeError(
                'Requires instance of TreeElement. '
                'Got {}'.format(type(child))
            )
        child.parent = self
        self._children.append(child)