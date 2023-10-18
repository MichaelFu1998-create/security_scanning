def get_locations(self):
        """
        Returns a list of locations.

        http://dev.wheniwork.com/#listing-locations
        """
        url = "/2/locations"

        data = self._get_resource(url)
        locations = []
        for entry in data['locations']:
            locations.append(self.location_from_json(entry))

        return locations