def store_populate_failed(cls, resource: str, session: Optional[Session] = None) -> 'Action':
        """Store a "populate failed" event.

        :param resource: The normalized name of the resource to store

        Example:

        >>> from bio2bel.models import Action
        >>> Action.store_populate_failed('hgnc')
        """
        action = cls.make_populate_failed(resource)
        _store_helper(action, session=session)
        return action