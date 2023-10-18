def aggregate_query(self, searchAreaWkt, agg_def, query=None, start_date=None, end_date=None, count=10, index=default_index):
        """Aggregates results of a query into buckets defined by the 'agg_def' parameter.  The aggregations are
        represented by dicts containing a 'name' key and a 'terms' key holding a list of the aggregation buckets.
        Each bucket element is a dict containing a 'term' key containing the term used for this bucket, a 'count' key
        containing the count of items that match this bucket, and an 'aggregations' key containing any child
        aggregations.

        Args:
            searchAreaWkt (str): wkt representation of the geometry
            agg_def (str or AggregationDef): the aggregation definitions
            query (str): a valid Elasticsearch query string to constrain the items going into the aggregation
            start_date (str): either an ISO-8601 date string or a 'now' expression (e.g. "now-6d" or just "now")
            end_date (str): either an ISO-8601 date string or a 'now' expression (e.g. "now-6d" or just "now")
            count (int): the number of buckets to include in the aggregations (the top N will be returned)
            index (str): the index (or alias or wildcard index expression) to run aggregations against, set to None for the entire set of vector indexes

        Returns:
            results (list): A (usually single-element) list of dict objects containing the aggregation results.
        """

        geojson = load_wkt(searchAreaWkt).__geo_interface__
        aggs_str = str(agg_def) # could be string or AggregationDef

        params = {
            "count": count,
            "aggs": aggs_str
        }

        if query:
            params['query'] = query
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        url = self.aggregations_by_index_url % index if index else self.aggregations_url

        r = self.gbdx_connection.post(url, params=params, json=geojson)
        r.raise_for_status()

        return r.json(object_pairs_hook=OrderedDict)['aggregations']