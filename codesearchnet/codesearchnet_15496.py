def update(self, scope, at=0):
        """Update scope. Add another scope to this one.
        Args:
            scope (Scope): Scope object
        Kwargs:
            at (int): Level to update
        """
        if hasattr(scope, '_mixins') and not at:
            self._mixins.update(scope._mixins)
        self[at]['__variables__'].update(scope[at]['__variables__'])
        self[at]['__blocks__'].extend(scope[at]['__blocks__'])
        self[at]['__names__'].extend(scope[at]['__names__'])