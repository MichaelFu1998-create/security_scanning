def retrieve(self, cursor):
        """
        Retrieve items from query
        """
        assert isinstance(cursor, dict), "expected cursor type 'dict'"

        # look for record in query
        query = self.get_query()
        assert isinstance(query, peewee.Query)

        query
        return query.get(**cursor)