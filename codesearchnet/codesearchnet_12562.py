def status(self, order_id):
        '''Checks imagery order status. There can be more than one image per
           order and this function returns the status of all images
           within the order.

           Args:
               order_id (str): The id of the order placed.

           Returns:
               List of dictionaries, one per image. Each dictionary consists
               of the keys 'acquisition_id', 'location' and 'state'.
        '''

        self.logger.debug('Get status of order ' + order_id)
        url = '%(base_url)s/order/%(order_id)s' % {
            'base_url': self.base_url, 'order_id': order_id
        }
        r = self.gbdx_connection.get(url)
        r.raise_for_status()
        return r.json().get("acquisitions", {})