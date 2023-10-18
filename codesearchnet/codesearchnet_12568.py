def search_point(self, lat, lng, filters=None, startDate=None, endDate=None, types=None, type=None):
        ''' Perform a catalog search over a specific point, specified by lat,lng

        Args:
            lat: latitude
            lng: longitude
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
        searchAreaWkt = "POLYGON ((%s %s, %s %s, %s %s, %s %s, %s %s))" % (lng, lat,lng,lat,lng,lat,lng,lat,lng,lat)
        return self.search(searchAreaWkt=searchAreaWkt, filters=filters, startDate=startDate, endDate=endDate, types=types)