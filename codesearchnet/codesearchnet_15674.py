def paginate_query(self, query, count, offset=None, sort=None):
        """
        Apply pagination to query

        :attr query: Instance of `peewee.Query`
        :attr count: Max rows to return
        :attr offset: Pagination offset, str/int
        :attr sort: List of tuples, e.g. [('id', 'asc')]

        :returns: Instance of `peewee.Query`
        """
        assert isinstance(query, peewee.Query)
        assert isinstance(count, int)
        assert isinstance(offset, (str, int, type(None)))
        assert isinstance(sort, (list, set, tuple, type(None)))

         # ensure our model has a primary key
        fields = query.model._meta.get_primary_keys()
        if len(fields) == 0:
            raise peewee.ProgrammingError(
                'Cannot apply pagination on model without primary key')

        # ensure our model doesn't use a compound primary key
        if len(fields) > 1:
            raise peewee.ProgrammingError(
                'Cannot apply pagination on model with compound primary key')

        # apply offset
        if offset is not None:
            query = query.where(fields[0] >= offset)

        # do we need to apply sorting?
        order_bys = []
        if sort:
            for field, direction in sort:
                # does this field have a valid sort direction?
                if not isinstance(direction, str):
                    raise ValueError("Invalid sort direction on field '{}'".format(field))

                direction = direction.lower().strip()
                if direction not in ['asc', 'desc']:
                    raise ValueError("Invalid sort direction on field '{}'".format(field))

                # apply sorting
                order_by = peewee.SQL(field)
                order_by = getattr(order_by, direction)()
                order_bys += [order_by]

        # add primary key ordering after user sorting
        order_bys += [fields[0].asc()]

        # apply ordering and limits
        query = query.order_by(*order_bys)
        query = query.limit(count)
        return query