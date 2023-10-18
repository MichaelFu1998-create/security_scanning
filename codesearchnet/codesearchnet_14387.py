def _call_api(self, verb, url, **request_kwargs):
        """Perform a github API call

        Args:
            verb (str): Can be "post", "put", or "get"
            url (str): The base URL with a leading slash for Github API (v3)
            auth (str or HTTPBasicAuth): A Github API token or a HTTPBasicAuth object
        """
        api = 'https://api.github.com{}'.format(url)
        auth_headers = {'Authorization': 'token {}'.format(self.api_token)}
        headers = {**auth_headers, **request_kwargs.pop('headers', {})}
        return getattr(requests, verb)(api, headers=headers, **request_kwargs)