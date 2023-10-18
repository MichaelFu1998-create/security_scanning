def new_bool(self, name=None, taint=frozenset(), avoid_collisions=False):
        """ Declares a free symbolic boolean in the constraint store
            :param name: try to assign name to internal variable representation,
                         if not unique, a numeric nonce will be appended
            :param avoid_collisions: potentially avoid_collisions the variable to avoid name collisions if True
            :return: a fresh BoolVariable
        """
        if name is None:
            name = 'B'
            avoid_collisions = True
        if avoid_collisions:
            name = self._make_unique_name(name)
        if not avoid_collisions and name in self._declarations:
            raise ValueError(f'Name {name} already used')
        var = BoolVariable(name, taint=taint)
        return self._declare(var)