async def get_tracks(self, query):
        """ Returns a Dictionary containing search results for a given query. """
        log.debug('Requesting tracks for query {}'.format(query))

        async with self.http.get(self.rest_uri + quote(query), headers={'Authorization': self.password}) as res:
            return await res.json(content_type=None)