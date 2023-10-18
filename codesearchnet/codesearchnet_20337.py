def format_parameters(self, **kwargs):
        """
        Properly formats array types
        """
        req_data = {}
        for k, v in kwargs.items():
            if isinstance(v, (list, tuple)):
                k = k + '[]'
            req_data[k] = v
        return req_data