def end(self, tag):
        """Handle an end tag.

        Call the handler's 'stream_end' method with
        an the root element (built by the `start` method).

        On the first level below root, sent the built element tree
        to the handler via the 'stanza methods'.

        Any tag below will be just added to the tree builder.
        """
        self._level -= 1
        if self._level < 0:
            self._handler.stream_parse_error(u"Unexpected end tag for: {0!r}"
                                                                .format(tag))
            return
        if self._level == 0:
            if tag != self._root.tag:
                self._handler.stream_parse_error(u"Unexpected end tag for:"
                            " {0!r} (stream end tag expected)".format(tag))
                return
            self._handler.stream_end()
            return
        element = self._builder.end(tag)
        if self._level == 1:
            self._handler.stream_element(element)