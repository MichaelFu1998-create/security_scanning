def get_func_argument_types(self, hsh: bytes):
        """Returns the tuple type signature for the arguments of the function associated with the selector ``hsh``.

        If no normal contract function has the specified selector,
        the empty tuple type signature ``'()'`` is returned.
        """
        if not isinstance(hsh, (bytes, bytearray)):
            raise TypeError('The selector argument must be a concrete byte array')
        sig = self._function_signatures_by_selector.get(hsh)
        return '()' if sig is None else sig[sig.find('('):]