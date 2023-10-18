def search(cls, query, q):
        """Modify query as so include only specific group names.

        :param query: Query object.
        :param str q: Search string.
        :returs: Query object.
        """
        return query.filter(Group.name.like('%{0}%'.format(q)))