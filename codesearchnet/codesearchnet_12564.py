def get(self, catID, includeRelationships=False):
        '''Retrieves the strip footprint WKT string given a cat ID.

        Args:
            catID (str): The source catalog ID from the platform catalog.
            includeRelationships (bool): whether to include graph links to related objects.  Default False.

        Returns:
            record (dict): A dict object identical to the json representation of the catalog record
        '''
        url = '%(base_url)s/record/%(catID)s' % {
            'base_url': self.base_url, 'catID': catID
        }
        r = self.gbdx_connection.get(url)
        r.raise_for_status()
        return r.json()