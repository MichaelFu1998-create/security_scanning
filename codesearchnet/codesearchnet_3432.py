def get_func_name(self, hsh: bytes) -> str:
        """Returns the name of the normal function with the selector ``hsh``,
        or ``'{fallback}'`` if no such function exists.
        """
        if not isinstance(hsh, (bytes, bytearray)):
            raise TypeError('The selector argument must be a concrete byte array')
        sig = self._function_signatures_by_selector.get(hsh)
        return '{fallback}' if sig is None else sig[:sig.find('(')]