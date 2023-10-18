def get_positions(self):
        """
        Returns a list of positions.

        http://dev.wheniwork.com/#listing-positions
        """
        url = "/2/positions"

        data = self._get_resource(url)
        positions = []
        for entry in data['positions']:
            positions.append(self.position_from_json(entry))

        return positions