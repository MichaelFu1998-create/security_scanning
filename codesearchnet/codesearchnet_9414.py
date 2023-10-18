def send_payload(self, params):
        """Performs the actual sending action and returns the result
        """
        data = json.dumps({
            'jsonrpc': self.version,
            'method': self.service_name,
            'params': params,
            'id': text_type(uuid.uuid4())
        })
        data_binary = data.encode('utf-8')
        url_request = Request(self.service_url, data_binary, headers=self.headers)
        return urlopen(url_request).read()