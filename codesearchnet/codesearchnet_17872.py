def query_by_names(cls, names):
        """Query group by a list of group names.

        :param list names: List of the group names.
        :returns: Query object.
        """
        assert isinstance(names, list)
        return cls.query.filter(cls.name.in_(names))