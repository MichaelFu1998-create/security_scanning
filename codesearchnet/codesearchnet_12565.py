def get_strip_metadata(self, catID):
        '''Retrieves the strip catalog metadata given a cat ID.

        Args:
            catID (str): The source catalog ID from the platform catalog.

        Returns:
            metadata (dict): A metadata dictionary .

            TODO: have this return a class object with interesting information exposed.
        '''

        self.logger.debug('Retrieving strip catalog metadata')
        url = '%(base_url)s/record/%(catID)s?includeRelationships=false' % {
            'base_url': self.base_url, 'catID': catID
        }
        r = self.gbdx_connection.get(url)
        if r.status_code == 200:
            return r.json()['properties']
        elif r.status_code == 404:
            self.logger.debug('Strip not found: %s' % catID)
            r.raise_for_status()
        else:
            self.logger.debug('There was a problem retrieving catid: %s' % catID)
            r.raise_for_status()