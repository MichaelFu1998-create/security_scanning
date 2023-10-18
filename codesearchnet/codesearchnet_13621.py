def send_stream_head(self, stanza_namespace, stream_from, stream_to,
                        stream_id = None, version = u'1.0', language = None):
        """
        Send stream head via the transport.

        :Parameters:
            - `stanza_namespace`: namespace of stream stanzas (e.g.
              'jabber:client')
            - `stream_from`: the 'from' attribute of the stream. May be `None`.
            - `stream_to`: the 'to' attribute of the stream. May be `None`.
            - `version`: the 'version' of the stream.
            - `language`: the 'xml:lang' of the stream
        :Types:
            - `stanza_namespace`: `unicode`
            - `stream_from`: `unicode`
            - `stream_to`: `unicode`
            - `version`: `unicode`
            - `language`: `unicode`
        """
        # pylint: disable=R0913
        with self.lock:
            self._serializer = XMPPSerializer(stanza_namespace,
                                            self.settings["extra_ns_prefixes"])
            head = self._serializer.emit_head(stream_from, stream_to,
                                                stream_id, version, language)
            self._write(head.encode("utf-8"))