def create_session(self):
        """Create a session on the frontier silicon device."""
        req_url = '%s/%s' % (self.__webfsapi, 'CREATE_SESSION')
        sid = yield from self.__session.get(req_url, params=dict(pin=self.pin),
                                            timeout = self.timeout)
        text = yield from sid.text(encoding='utf-8')
        doc = objectify.fromstring(text)
        return doc.sessionId.text