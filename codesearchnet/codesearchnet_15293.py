def store_drop(cls, resource: str, session: Optional[Session] = None) -> 'Action':
        """Store a "drop" event.

        :param resource: The normalized name of the resource to store

        Example:

        >>> from bio2bel.models import Action
        >>> Action.store_drop('hgnc')
        """
        action = cls.make_drop(resource)
        _store_helper(action, session=session)
        return action