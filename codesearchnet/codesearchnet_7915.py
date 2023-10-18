def encode_payload(self, messages):
        """Encode list of messages. Expects messages to be unicode.

        ``messages`` - List of raw messages to encode, if necessary

        """
        if not messages or messages[0] is None:
            return ''

        if len(messages) == 1:
            return messages[0].encode('utf-8')

        payload = u''.join([(u'\ufffd%d\ufffd%s' % (len(p), p))
                            for p in messages if p is not None])
        # FIXME: why is it so that we must filter None from here ?  How
        #        is it even possible that a None gets in there ?

        return payload.encode('utf-8')