def make_upstream_request(self):
        "Return request object for calling the upstream"
        url = self.upstream_url(self.request.uri)
        return tornado.httpclient.HTTPRequest(url,
            method=self.request.method,
            headers=self.request.headers,
            body=self.request.body if self.request.body else None)