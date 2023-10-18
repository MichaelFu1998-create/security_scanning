def create(self, data):
        """
        Begin processing a batch operations request.

        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "operations": array*
            [
                {
                    "method": string* (Must be one of "GET", "POST", "PUT", "PATCH", or "DELETE")
                    "path": string*,
                }
            ]
        }
        """
        if 'operations' not in data:
            raise KeyError('The batch must have operations')
        for op in data['operations']:
            if 'method' not in op:
                raise KeyError('The batch operation must have a method')
            if op['method'] not in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                raise ValueError('The batch operation method must be one of "GET", "POST", "PUT", "PATCH", '
                                 'or "DELETE", not {0}'.format(op['method']))
            if 'path' not in op:
                raise KeyError('The batch operation must have a path')
        return self._mc_client._post(url=self._build_path(), data=data)