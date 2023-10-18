def _filter(cls, query, state=MembershipState.ACTIVE, eager=None):
        """Filter a query result."""
        query = query.filter_by(state=state)

        eager = eager or []
        for field in eager:
            query = query.options(joinedload(field))

        return query