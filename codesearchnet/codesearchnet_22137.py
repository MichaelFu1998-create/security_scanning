def create_position(self, params={}):
        """
        Creates a position

        http://dev.wheniwork.com/#create-update-position
        """
        url = "/2/positions/"
        body = params

        data = self._post_resource(url, body)
        return self.position_from_json(data["position"])