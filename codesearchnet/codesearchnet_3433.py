def get_func_signature(self, hsh: bytes) -> Optional[str]:
        """Returns the signature of the normal function with the selector ``hsh``,
        or ``None`` if no such function exists.

        This function returns ``None`` for any selector that will be dispatched to a fallback function.
        """
        if not isinstance(hsh, (bytes, bytearray)):
            raise TypeError('The selector argument must be a concrete byte array')
        return self._function_signatures_by_selector.get(hsh)