def send_request(self, kind, url_components, **kwargs):
        """
        Send a request for this resource to the API

        Parameters
        ----------
        kind: str, {'get', 'delete', 'put', 'post', 'head'}
        """
        return self.api.send_request(kind, self.resource_path, url_components,
                                     **kwargs)