def get_location(self, location_id, depth=0):
        """
        Retrieves a single location by ID.

        :param      location_id: The unique ID of the location.
        :type       location_id: ``str``

        """
        response = self._perform_request('/locations/%s?depth=%s' % (location_id, depth))
        return response