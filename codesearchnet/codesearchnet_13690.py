def stream_start(self, element):
        """Process <stream:stream> (stream start) tag received from peer.

        `lock` is acquired when this method is called.

        :Parameters:
            - `element`: root element (empty) created by the parser"""
        with self.lock:
            logger.debug("input document: " + element_to_unicode(element))
            if not element.tag.startswith(STREAM_QNP):
                self._send_stream_error("invalid-namespace")
                raise FatalStreamError("Bad stream namespace")
            if element.tag != STREAM_ROOT_TAG:
                self._send_stream_error("bad-format")
                raise FatalStreamError("Bad root element")

            if self._input_state == "restart":
                event = StreamRestartedEvent(self.peer)
            else:
                event = StreamConnectedEvent(self.peer)
            self._input_state = "open"
            version = element.get("version")
            if version:
                try:
                    major, minor = version.split(".", 1)
                    major, minor = int(major), int(minor)
                except ValueError:
                    self._send_stream_error("unsupported-version")
                    raise FatalStreamError("Unsupported protocol version.")
                self.version = (major, minor)
            else:
                self.version = (0, 9)

            if self.version[0] != 1 and self.version != (0, 9):
                self._send_stream_error("unsupported-version")
                raise FatalStreamError("Unsupported protocol version.")

            peer_lang = element.get(XML_LANG_QNAME)
            self.peer_language = peer_lang
            if not self.initiator:
                lang = None
                languages = self.settings["languages"]
                while peer_lang:
                    if peer_lang in languages:
                        lang = peer_lang
                        break
                    match = LANG_SPLIT_RE.match(peer_lang)
                    if not match:
                        break
                    peer_lang = match.group(0)
                if lang:
                    self.language = lang

            if self.initiator:
                self.stream_id = element.get("id")
                peer = element.get("from")
                if peer:
                    peer = JID(peer)
                if self.peer:
                    if peer and peer != self.peer:
                        logger.debug("peer hostname mismatch: {0!r} != {1!r}"
                                                    .format(peer, self.peer))
                self.peer = peer
            else:
                to = element.get("to")
                if to:
                    to = self.check_to(to)
                    if not to:
                        self._send_stream_error("host-unknown")
                        raise FatalStreamError('Bad "to"')
                    self.me = JID(to)
                peer = element.get("from")
                if peer:
                    peer = JID(peer)
                self._send_stream_start(self.generate_id(), stream_to = peer)
                self._send_stream_features()
            self.event(event)