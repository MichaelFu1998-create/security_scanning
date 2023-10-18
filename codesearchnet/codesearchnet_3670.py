def new_array(self, index_bits=32, name=None, index_max=None, value_bits=8, taint=frozenset(), avoid_collisions=False, default=None):
        """ Declares a free symbolic array of value_bits long bitvectors in the constraint store.
            :param index_bits: size in bits for the array indexes one of [32, 64]
            :param value_bits: size in bits for the array values
            :param name: try to assign name to internal variable representation,
                         if not unique, a numeric nonce will be appended
            :param index_max: upper limit for indexes on this array (#FIXME)
            :param avoid_collisions: potentially avoid_collisions the variable to avoid name collisions if True
            :param default: default for not initialized values
            :return: a fresh ArrayProxy
        """
        if name is None:
            name = 'A'
            avoid_collisions = True
        if avoid_collisions:
            name = self._make_unique_name(name)
        if not avoid_collisions and name in self._declarations:
            raise ValueError(f'Name {name} already used')
        var = self._declare(ArrayVariable(index_bits, index_max, value_bits, name, taint=taint))
        return ArrayProxy(var, default=default)