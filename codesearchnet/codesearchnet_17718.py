def get_time_estimate(self, start_latitude, start_longitude, customer_uuid=None, product_id=None):
        """
        Get the ETA for Uber products.
        :param start_latitude: Starting latitude.
        :param start_longitude: Starting longitude.
        :param customer_uuid: (Optional) Customer unique ID.
        :param product_id: (Optional) If ETA is needed only for a specific product type.
        :return: JSON
        """

        endpoint = 'estimates/time'
        query_parameters = {
            'start_latitude': start_latitude,
            'start_longitude': start_longitude
        }

        if customer_uuid is not None:
            query_parameters['customer_uuid'] = customer_uuid
        elif product_id is not None:
            query_parameters['product_id'] = product_id
        elif customer_uuid is not None and product_id is not None:
            query_parameters['customer_uuid'] = customer_uuid
            query_parameters['product_id'] = product_id

        return self.get_json(endpoint, 'GET', query_parameters, None, None)