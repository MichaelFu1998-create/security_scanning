def _handle_request(self, scheme, netloc, path, headers, body=None, method="GET"):
        """
        Run the actual request
        """
        backend_url = "{}://{}{}".format(scheme, netloc, path)
        try:
            response = self.http_request.request(backend_url, method=method, body=body, headers=dict(headers))
            self._return_response(response)
        except Exception as e:
            body = "Invalid response from backend: '{}' Server might be busy".format(e.message)
            logging.debug(body)
            self.send_error(httplib.SERVICE_UNAVAILABLE, body)