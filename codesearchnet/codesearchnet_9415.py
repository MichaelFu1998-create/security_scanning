def make_response(self, rv):
        """Converts the return value from a view function to a real
        response object that is an instance of :attr:`response_class`.
        """
        status_or_headers = headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))

        if rv is None:
            raise ValueError('View function did not return a response')

        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None

        D = json.loads(extract_raw_data_request(request))
        if type(D) is list:
            raise InvalidRequestError('JSON-RPC batch with decorator (make_response) not is supported')
        else:
            response_obj = self.empty_response(version=D['jsonrpc'])
            response_obj['id'] = D['id']
            response_obj['result'] = rv
            response_obj.pop('error', None)
            rv = jsonify(response_obj)

        if status_or_headers is not None:
            if isinstance(status_or_headers, string_types):
                rv.status = status_or_headers
            else:
                rv.status_code = status_or_headers
        if headers:
            rv.headers.extend(headers)

        return rv