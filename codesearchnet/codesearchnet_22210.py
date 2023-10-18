def _delete_resource(self, url):
        """
        When I Work DELETE method.
        """
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        if self.token:
            headers["W-Token"] = "%s" % self.token
        response = WhenIWork_DAO().deleteURL(url, headers)

        if not (response.status == 200 or response.status == 201 or
                response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)