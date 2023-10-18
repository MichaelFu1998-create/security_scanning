def get_position(self, position_id):
        """
        Returns position data.

        http://dev.wheniwork.com/#get-existing-position
        """
        url = "/2/positions/%s" % position_id

        return self.position_from_json(self._get_resource(url)["position"])