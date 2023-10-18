def write(self, address, value, force=False):
        """
        Write a value at address.
        :param address: The address at which to write
        :type address: int or long or Expression
        :param value: Bytes to write
        :type value: str or list
        :param force: Whether to ignore permissions
        """
        size = len(value)
        if issymbolic(address):

            solutions = self._try_get_solutions(address, size, 'w', force=force)

            for offset in range(size):
                for base in solutions:
                    condition = base == address
                    self._symbols.setdefault(base + offset, []).append((condition, value[offset]))
        else:

            for offset in range(size):
                if issymbolic(value[offset]):
                    if not self.access_ok(address + offset, 'w', force):
                        raise InvalidMemoryAccess(address + offset, 'w')
                    self._symbols[address + offset] = [(True, value[offset])]
                else:
                    # overwrite all previous items
                    if address + offset in self._symbols:
                        del self._symbols[address + offset]
                    super().write(address + offset, [value[offset]], force)