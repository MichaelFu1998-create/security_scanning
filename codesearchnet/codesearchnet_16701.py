def node(self, *args, **kwargs):
        """Return a :class:`CellNode` object for the given arguments."""
        return CellNode(get_node(self._impl, *convert_args(args, kwargs)))