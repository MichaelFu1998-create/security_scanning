def _get_resource(self, url, data_key=None):
        """
        When I Work GET method. Return representation of the requested
        resource.
        """
        headers = {"Accept": "application/json"}
        if self.token:
            headers["W-Token"] = "%s" % self.token
        response = WhenIWork_DAO().getURL(url, headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)