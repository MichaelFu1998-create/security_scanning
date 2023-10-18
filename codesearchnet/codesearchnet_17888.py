def search(cls, query, q):
        """Modify query as so include only specific members.

        :param query: Query object.
        :param str q: Search string.
        :returs: Query object.
        """
        query = query.join(User).filter(
                User.email.like('%{0}%'.format(q)),
        )
        return query