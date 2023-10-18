def order(cls, query, field, s):
        """Modify query as so to order the results.

        :param query: Query object.
        :param str s: Orderinig: ``asc`` or ``desc``.
        :returs: Query object.
        """
        if s == 'asc':
            query = query.order_by(asc(field))
        elif s == 'desc':
            query = query.order_by(desc(field))
        return query