def start(self, tag, attrs):
        """Handle the start tag.

        Call the handler's 'stream_start' methods with
        an empty root element if it is top level.

        For lower level tags use :etree:`ElementTree.TreeBuilder` to collect
        them.
        """
        if self._level == 0:
            self._root = ElementTree.Element(tag, attrs)
            self._handler.stream_start(self._root)
        if self._level < 2:
            self._builder = ElementTree.TreeBuilder()
        self._level += 1
        return self._builder.start(tag, attrs)