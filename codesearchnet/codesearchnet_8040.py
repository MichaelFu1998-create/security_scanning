def search(self, query):
        """
        Search the index for a given query, and return a result of documents

        ### Parameters

        - **query**: the search query. Either a text for simple queries with default parameters, or a Query object for complex queries.
                     See RediSearch's documentation on query format
        - **snippet_sizes**: A dictionary of {field: snippet_size} used to trim and format the result. e.g.e {'body': 500}
        """
        args, query = self._mk_query_args(query)
        st = time.time()
        res = self.redis.execute_command(self.SEARCH_CMD, *args)

        return Result(res,
                      not query._no_content,
                      duration=(time.time() - st) * 1000.0,
                      has_payload=query._with_payloads)