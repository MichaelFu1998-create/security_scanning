def _execute_search_query(self, returning_query, result_class):
        """
        Run a PIF query against Citrination.

        :param returning_query: :class:`BaseReturningQuery` to execute.
        :param result_class: The class of the result to return.
        :return: ``result_class`` object with the results of the query.
        """
        if returning_query.from_index:
            from_index = returning_query.from_index
        else:
            from_index = 0

        if returning_query.size != None:
            size = min(returning_query.size, client_config.max_query_size)
        else:
            size = client_config.max_query_size

        if (size == client_config.max_query_size and
                    size != returning_query.size):
            self._warn("Query size greater than max system size - only {} results will be returned".format(size))

        time = 0.0;
        hits = [];
        while True:
            sub_query = deepcopy(returning_query)
            sub_query.from_index = from_index + len(hits)
            partial_results = self._search_internal(sub_query, result_class)
            total = partial_results.total_num_hits
            time += partial_results.took
            if partial_results.hits is not None:
                hits.extend(partial_results.hits)
            if len(hits) >= size or len(hits) >= total or sub_query.from_index >= total:
                break

        return result_class(hits=hits, total_num_hits=total, took=time)