def limit(self, offset, num):
        """
        Sets the limit for the most recent group or query.

        If no group has been defined yet (via `group_by()`) then this sets
        the limit for the initial pool of results from the query. Otherwise,
        this limits the number of items operated on from the previous group.

        Setting a limit on the initial search results may be useful when
        attempting to execute an aggregation on a sample of a large data set.

        ### Parameters

        - **offset**: Result offset from which to begin paging
        - **num**: Number of results to return


        Example of sorting the initial results:

        ```
        AggregateRequest('@sale_amount:[10000, inf]')\
            .limit(0, 10)\
            .group_by('@state', r.count())
        ```

        Will only group by the states found in the first 10 results of the
        query `@sale_amount:[10000, inf]`. On the other hand,

        ```
        AggregateRequest('@sale_amount:[10000, inf]')\
            .limit(0, 1000)\
            .group_by('@state', r.count()\
            .limit(0, 10)
        ```

        Will group all the results matching the query, but only return the
        first 10 groups.

        If you only wish to return a *top-N* style query, consider using
        `sort_by()` instead.

        """
        limit = Limit(offset, num)
        if self._groups:
            self._groups[-1].limit = limit
        else:
            self._limit = limit
        return self