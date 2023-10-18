def emit_head(self, stream_from, stream_to, stream_id = None,
                                            version = u'1.0', language = None):
        """Return the opening tag of the stream root element.

        :Parameters:
            - `stream_from`: the 'from' attribute of the stream. May be `None`.
            - `stream_to`: the 'to' attribute of the stream. May be `None`.
            - `version`: the 'version' of the stream.
            - `language`: the 'xml:lang' of the stream
        :Types:
            - `stream_from`: `unicode`
            - `stream_to`: `unicode`
            - `version`: `unicode`
            - `language`: `unicode`
        """
        # pylint: disable-msg=R0913
        self._root_prefixes = dict(STANDARD_PREFIXES)
        self._root_prefixes[self.stanza_namespace] = None
        for namespace, prefix in self._root_prefixes.items():
            if not prefix or prefix == "stream":
                continue
            if namespace in STANDARD_PREFIXES or namespace in STANZA_NAMESPACES:
                continue
            self._root_prefixes[namespace] = prefix
        tag = u"<{0}:stream version={1}".format(STANDARD_PREFIXES[STREAM_NS],
                                                        quoteattr(version))
        if stream_from:
            tag += u" from={0}".format(quoteattr(stream_from))
        if stream_to:
            tag += u" to={0}".format(quoteattr(stream_to))
        if stream_id is not None:
            tag += u" id={0}".format(quoteattr(stream_id))
        if language is not None:
            tag += u" xml:lang={0}".format(quoteattr(language))
        for namespace, prefix in self._root_prefixes.items():
            if prefix == "xml":
                continue
            if prefix:
                tag += u' xmlns:{0}={1}'.format(prefix, quoteattr(namespace))
            else:
                tag += u' xmlns={1}'.format(prefix, quoteattr(namespace))
        tag += u">"
        self._head_emitted = True
        return tag