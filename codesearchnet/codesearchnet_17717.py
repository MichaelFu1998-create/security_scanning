def get_price_estimate(self, start_latitude, start_longitude, end_latitude, end_longitude):
        """
        Returns the fare estimate based on two sets of coordinates.
        :param start_latitude: Starting latitude or latitude of pickup address.
        :param start_longitude: Starting longitude or longitude of pickup address.
        :param end_latitude: Ending latitude or latitude of destination address.
        :param end_longitude: Ending longitude or longitude of destination address.
        :return: JSON
        """
        endpoint = 'estimates/price'
        query_parameters = {
            'start_latitude': start_latitude,
            'start_longitude': start_longitude,
            'end_latitude': end_latitude,
            'end_longitude': end_longitude
        }

        return self.get_json(endpoint, 'GET', query_parameters, None, None)