def search(self, searchAreaWkt=None, filters=None, startDate=None, endDate=None, types=None):
        ''' Perform a catalog search

        Args:
            searchAreaWkt: WKT Polygon of area to search.  Optional.
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
        # Default to search for Acquisition type objects.
        if not types:
            types = ['Acquisition']

        # validation:  we must have either a WKT or one-week of time window
        if startDate:
            startDateTime = datetime.datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S.%fZ')

        if endDate:
            endDateTime = datetime.datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S.%fZ')

        if startDate and endDate:
            diff = endDateTime - startDateTime
            if diff.days < 0:
                raise Exception("startDate must come before endDate.")

        postdata = {
            "searchAreaWkt": searchAreaWkt,
            "types": types,
            "startDate": startDate,
            "endDate": endDate,
        }

        if filters:
            postdata['filters'] = filters

        if searchAreaWkt:
            postdata['searchAreaWkt'] = searchAreaWkt

        url = '%(base_url)s/search' % {
            'base_url': self.base_url
        }
        headers = {'Content-Type':'application/json'}
        r = self.gbdx_connection.post(url, headers=headers, data=json.dumps(postdata))
        r.raise_for_status()
        results = r.json()['results']

        return results