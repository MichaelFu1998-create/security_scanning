def search_address(self, address, filters=None, startDate=None, endDate=None, types=None):
        ''' Perform a catalog search over an address string

        Args:
            address: any address string
            filters: Array of filters.  Optional.  Example:
            [
                "(sensorPlatformName = 'WORLDVIEW01' OR sensorPlatformName ='QUICKBIRD02')",
                "cloudCover < 10",
                "offNadirAngle < 10"
            ]
            startDate: string.  Optional.  Example: "2004-01-01T00:00:00.000Z"
            endDate: string.  Optional.  Example: "2004-01-01T00:00:00.000Z"
            types: Array of types to search for.  Optional.  Example (and default):  ["Acquisition"]

        Returns:
            catalog search resultset
        '''
        lat, lng = self.get_address_coords(address)
        return self.search_point(lat,lng, filters=filters, startDate=startDate, endDate=endDate, types=types)