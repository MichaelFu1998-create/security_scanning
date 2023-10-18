def get_fsapi_endpoint(self):
        """Parse the fsapi endpoint from the device url."""
        endpoint = yield from self.__session.get(self.fsapi_device_url, timeout = self.timeout)
        text = yield from endpoint.text(encoding='utf-8')
        doc = objectify.fromstring(text)
        return doc.webfsapi.text