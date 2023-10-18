def store_populate(cls, resource: str, session: Optional[Session] = None) -> 'Action':
        """Store a "populate" event.

        :param resource: The normalized name of the resource to store

        Example:

        >>> from bio2bel.models import Action
        >>> Action.store_populate('hgnc')
        """
        action = cls.make_populate(resource)
        _store_helper(action, session=session)
        return action