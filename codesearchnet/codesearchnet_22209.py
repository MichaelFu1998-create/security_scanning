def _post_resource(self, url, body):
        """
        When I Work POST method.
        """
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        if self.token:
            headers["W-Token"] = "%s" % self.token
        response = WhenIWork_DAO().postURL(url, headers, json.dumps(body))

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)