def __exchange(self, output, timeout=None):
        """Write output to the port and wait for response"""
        self.__writeln(output)
        self._port.flush()
        return self.__expect(timeout=timeout or self._timeout)