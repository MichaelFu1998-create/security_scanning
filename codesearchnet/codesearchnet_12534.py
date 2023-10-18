def query(self, searchAreaWkt, query, count=100, ttl='5m', index=default_index):
        '''
        Perform a vector services query using the QUERY API
        (https://gbdxdocs.digitalglobe.com/docs/vs-query-list-vector-items-returns-default-fields)

        Args:
            searchAreaWkt: WKT Polygon of area to search
            query: Elastic Search query
            count: Maximum number of results to return
            ttl: Amount of time for each temporary vector page to exist

        Returns:
            List of vector results
    
        '''
        if count < 1000:
            # issue a single page query
            search_area_polygon = from_wkt(searchAreaWkt)
            left, lower, right, upper = search_area_polygon.bounds

            params = {
                "q": query,
                "count": min(count,1000),
                "left": left,
                "right": right,
                "lower": lower,
                "upper": upper
            }

            url = self.query_index_url % index if index else self.query_url
            r = self.gbdx_connection.get(url, params=params)
            r.raise_for_status()
            return r.json()
        else:
            return list(self.query_iteratively(searchAreaWkt, query, count, ttl, index))