def sort_by(self, *fields, **kwargs):
        """
        Indicate how the results should be sorted. This can also be used for
        *top-N* style queries

        ### Parameters

        - **fields**: The fields by which to sort. This can be either a single
            field or a list of fields. If you wish to specify order, you can
            use the `Asc` or `Desc` wrapper classes.
        - **max**: Maximum number of results to return. This can be used instead
            of `LIMIT` and is also faster.


        Example of sorting by `foo` ascending and `bar` descending:

        ```
        sort_by(Asc('@foo'), Desc('@bar'))
        ```

        Return the top 10 customers:

        ```
        AggregateRequest()\
            .group_by('@customer', r.sum('@paid').alias(FIELDNAME))\
            .sort_by(Desc('@paid'), max=10)
        ```
        """
        self._max = kwargs.get('max', 0)
        if isinstance(fields, (string_types, SortDirection)):
            fields = [fields]
        for f in fields:
            if isinstance(f, SortDirection):
                self._sortby += [f.field, f.DIRSTRING]
            else:
                self._sortby.append(f)
        return self