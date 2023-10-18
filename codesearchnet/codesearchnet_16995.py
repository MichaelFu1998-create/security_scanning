def _return_response(self, response):
        """
        :type result: HTTPResponse
        """
        self.filter_headers(response.msg)
        if "content-length" in response.msg:
            del response.msg["content-length"]

        self.send_response(response.status, response.reason)
        for header_key, header_value in response.msg.items():
            self.send_header(header_key, header_value)
        body = response.read()
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)