def get_location(self, location_id):
        """
        Returns location data.

        http://dev.wheniwork.com/#get-existing-location
        """
        url = "/2/locations/%s" % location_id

        return self.location_from_json(self._get_resource(url)["location"])