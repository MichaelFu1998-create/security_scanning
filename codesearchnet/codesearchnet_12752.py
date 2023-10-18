async def prepare_request(self, method, url,
                              headers=None,
                              skip_params=False,
                              proxy=None,
                              **kwargs):
        """
        prepare all the arguments for the request

        Parameters
        ----------
        method : str
            HTTP method used by the request
        url : str
            The url to request
        headers : dict, optional
            Additionnal headers
        proxy : str
            proxy of the request
        skip_params : bool
            Don't use the parameters to sign the request

        Returns
        -------
        dict
            Parameters of the request correctly formatted
        """

        if method.lower() == "post":
            key = 'data'
        else:
            key = 'params'

        if key in kwargs and not skip_params:
            request_params = {key: kwargs.pop(key)}
        else:
            request_params = {}

        request_params.update(dict(method=method.upper(), url=url))

        coro = self.sign(**request_params, skip_params=skip_params,
                         headers=headers)
        request_params['headers'] = await utils.execute(coro)
        request_params['proxy'] = proxy

        kwargs.update(request_params)

        return kwargs