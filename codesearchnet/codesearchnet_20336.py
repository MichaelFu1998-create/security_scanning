def send_request(self, kind, resource, url_components, **kwargs):
        """
        Send a request to the REST API

        Parameters
        ----------
        kind: str, {get, delete, put, post, head}
        resource: str
        url_components: list or tuple to be appended to the request URL

        Notes
        -----
        kwargs contain request parameters to be sent as request data
        """
        url = self.format_request_url(resource, *url_components)
        meth = getattr(requests, kind)
        headers = self.get_request_headers()
        req_data = self.format_parameters(**kwargs)
        response = meth(url, headers=headers, data=req_data)
        data = self.get_response(response)
        if response.status_code >= 300:
            msg = data.pop('message', 'API request returned error')
            raise APIError(msg, response.status_code, **data)
        return data