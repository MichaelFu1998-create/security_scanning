def query_iteratively(self, searchAreaWkt, query, count=100, ttl='5m', index=default_index):
        '''
        Perform a vector services query using the QUERY API
        (https://gbdxdocs.digitalglobe.com/docs/vs-query-list-vector-items-returns-default-fields)

        Args:
            searchAreaWkt: WKT Polygon of area to search
            query: Elastic Search query
            count: Maximum number of results to return
            ttl: Amount of time for each temporary vector page to exist

        Returns:
            generator of vector results
    
        '''

        search_area_polygon = from_wkt(searchAreaWkt)
        left, lower, right, upper = search_area_polygon.bounds

        params = {
            "q": query,
            "count": min(count,1000),
            "ttl": ttl,
            "left": left,
            "right": right,
            "lower": lower,
            "upper": upper
        }

        # initialize paging request
        url = self.query_index_page_url % index if index else self.query_page_url
        r = self.gbdx_connection.get(url, params=params)
        r.raise_for_status()
        page = r.json()
        paging_id = page['next_paging_id']
        item_count = int(page['item_count'])
        data = page['data']


        num_results = 0
        for vector in data:
          num_results += 1
          if num_results > count: break
          yield vector

        if num_results == count:
          return


        # get vectors from each page
        while paging_id and item_count > 0 and num_results < count:

          headers = {'Content-Type':'application/x-www-form-urlencoded'}
          data = {
              "pagingId": paging_id,
              "ttl": ttl
          }

          r = self.gbdx_connection.post(self.page_url, headers=headers, data=data)
          r.raise_for_status()
          page = r.json()
          paging_id = page['next_paging_id']
          item_count = int(page['item_count'])
          data = page['data']

          for vector in data:
              num_results += 1
              if num_results > count: break
              yield vector