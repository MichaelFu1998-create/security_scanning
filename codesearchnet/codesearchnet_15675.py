def apply_filters(self, query, filters):
        """
        Apply user specified filters to query
        """
        assert isinstance(query, peewee.Query)
        assert isinstance(filters, dict)