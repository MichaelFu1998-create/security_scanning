def delete(self, config_object, purge=None, recurse=False):
        """
        send a delete request
        XXX [more here]
        """
        rest_url = config_object.href
        params = []

        # purge deletes the SLD from disk when a style is deleted
        if purge:
            params.append("purge=" + str(purge))

        # recurse deletes the resource when a layer is deleted.
        if recurse:
            params.append("recurse=true")

        if params:
            rest_url = rest_url + "?" + "&".join(params)

        headers = {
            "Content-type": "application/xml",
            "Accept": "application/xml"
        }

        resp = self.http_request(rest_url, method='delete', headers=headers)
        if resp.status_code != 200:
            raise FailedRequestError('Failed to make DELETE request: {}, {}'.format(resp.status_code, resp.text))

        self._cache.clear()

        # do we really need to return anything other than None?
        return (resp)