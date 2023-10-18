def call(self, path, extra=None):
        """Execute a frontier silicon API call."""
        try:
            if not self.__webfsapi:
                self.__webfsapi = yield from self.get_fsapi_endpoint()

            if not self.sid:
                self.sid = yield from self.create_session()

            if not isinstance(extra, dict):
                extra = dict()

            params = dict(pin=self.pin, sid=self.sid)
            params.update(**extra)

            req_url = ('%s/%s' % (self.__webfsapi, path))
            result = yield from self.__session.get(req_url, params=params,
                                                   timeout = self.timeout)
            if result.status == 200:
                text = yield from result.text(encoding='utf-8')
            else:
                self.sid = yield from self.create_session()
                params = dict(pin=self.pin, sid=self.sid)
                params.update(**extra)
                result = yield from self.__session.get(req_url, params=params,
                                                       timeout = self.timeout)
                text = yield from result.text(encoding='utf-8')

            return objectify.fromstring(text)
        except Exception as e:
            logging.info('AFSAPI Exception: ' +traceback.format_exc())

        return None