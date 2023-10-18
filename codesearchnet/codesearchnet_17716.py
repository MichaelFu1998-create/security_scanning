def get_products(self, latitude, longitude):
        """
        Get a list of all Uber products based on latitude and longitude coordinates.
        :param latitude: Latitude for which product list is required.
        :param longitude: Longitude for which product list is required.
        :return: JSON
        """
        endpoint = 'products'
        query_parameters = {
            'latitude': latitude,
            'longitude': longitude
        }

        return self.get_json(endpoint, 'GET', query_parameters, None, None)