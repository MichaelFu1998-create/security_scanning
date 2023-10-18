def _process_element(self, element):
        """Process first level element of the stream.

        The element may be stream error or features, StartTLS
        request/response, SASL request/response or a stanza.

        :Parameters:
            - `element`: XML element
        :Types:
            - `element`: :etree:`ElementTree.Element`
        """
        tag = element.tag
        if tag in self._element_handlers:
            handler = self._element_handlers[tag]
            logger.debug("Passing element {0!r} to method {1!r}"
                                                .format(element, handler))
            handled = handler(self, element)
            if handled:
                return
        if tag.startswith(self._stanza_namespace_p):
            stanza = stanza_factory(element, self, self.language)
            self.uplink_receive(stanza)
        elif tag == ERROR_TAG:
            error = StreamErrorElement(element)
            self.process_stream_error(error)
        elif tag == FEATURES_TAG:
            logger.debug("Got features element: {0}".format(serialize(element)))
            self._got_features(element)
        else:
            logger.debug("Unhandled element: {0}".format(serialize(element)))
            logger.debug(" known handlers: {0!r}".format(
                                                    self._element_handlers))