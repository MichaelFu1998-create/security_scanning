def new_bitvec(self, size, name=None, taint=frozenset(), avoid_collisions=False):
        """ Declares a free symbolic bitvector in the constraint store
            :param size: size in bits for the bitvector
            :param name: try to assign name to internal variable representation,
                         if not unique, a numeric nonce will be appended
            :param avoid_collisions: potentially avoid_collisions the variable to avoid name collisions if True
            :return: a fresh BitVecVariable
        """
        if not (size == 1 or size % 8 == 0):
            raise Exception(f'Invalid bitvec size {size}')
        if name is None:
            name = 'BV'
            avoid_collisions = True
        if avoid_collisions:
            name = self._make_unique_name(name)
        if not avoid_collisions and name in self._declarations:
            raise ValueError(f'Name {name} already used')
        var = BitVecVariable(size, name, taint=taint)
        return self._declare(var)