def aggregate(self, query):
        """
        Issue an aggregation query

        ### Parameters

        **query**: This can be either an `AggeregateRequest`, or a `Cursor`

        An `AggregateResult` object is returned. You can access the rows from its
        `rows` property, which will always yield the rows of the result
        """
        if isinstance(query, AggregateRequest):
            has_schema = query._with_schema
            has_cursor = bool(query._cursor)
            cmd = [self.AGGREGATE_CMD, self.index_name] + query.build_args()
        elif isinstance(query, Cursor):
            has_schema = False
            has_cursor = True
            cmd = [self.CURSOR_CMD, 'READ', self.index_name] + query.build_args()
        else:
            raise ValueError('Bad query', query)

        raw = self.redis.execute_command(*cmd)
        if has_cursor:
            if isinstance(query, Cursor):
                query.cid = raw[1]
                cursor = query
            else:
                cursor = Cursor(raw[1])
            raw = raw[0]
        else:
            cursor = None

        if query._with_schema:
            schema = raw[0]
            rows = raw[2:]
        else:
            schema = None
            rows = raw[1:]

        res = AggregateResult(rows, cursor, schema)
        return res