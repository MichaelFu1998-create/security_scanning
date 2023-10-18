def get_most_recent_images(self, results, types=[], sensors=[], N=1):
        ''' Return the most recent image

        Args:
            results: a catalog resultset, as returned from a search
            types: array of types you want. optional.
            sensors: array of sensornames. optional.
            N: number of recent images to return.  defaults to 1.

        Returns:
            single catalog item, or none if not found

        '''
        if not len(results):
            return None

        # filter on type
        if types:
            results = [r for r in results if r['type'] in types]

        # filter on sensor
        if sensors:
            results = [r for r in results if r['properties'].get('sensorPlatformName') in sensors]


        # sort by date:
        #sorted(results, key=results.__getitem__('properties').get('timestamp'))
        newlist = sorted(results, key=lambda k: k['properties'].get('timestamp'), reverse=True)
        return newlist[:N]